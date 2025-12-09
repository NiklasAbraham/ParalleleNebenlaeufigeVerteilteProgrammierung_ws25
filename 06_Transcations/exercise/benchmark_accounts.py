#!/usr/bin/env python3
"""Benchmark Haskell STM vs Go Locks. Save results to CSV and plot."""

import csv
import shutil
import statistics
import subprocess
import tempfile
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.absolute()
GO_DIR = SCRIPT_DIR.parent.parent / "05_Channels" / "exercise" / "accounts"


def create_haskell(num_accounts, num_iterations, max_amount, output_file):
    """Create parameterized Haskell program."""
    content = f"""{{-# LANGUAGE BlockArguments #-}}

import Control.Concurrent
import Control.Concurrent.STM
import Control.Concurrent.STM.TArray
import Control.Monad
import Data.Array.MArray
import System.Random

transfer :: TArray Int Int -> Int -> Int -> Int -> STM ()
transfer accounts amount source target = do
  sourceBalance <- readArray accounts source
  if sourceBalance < amount
    then retry
    else do
      writeArray accounts source (sourceBalance - amount)
      targetBalance <- readArray accounts target
      writeArray accounts target (targetBalance + amount)

waitGroupAdd :: TVar Int -> IO ()
waitGroupAdd counter = atomically do
  modifyTVar counter (+1)

waitGroupDone :: TVar Int -> IO ()
waitGroupDone counter = atomically do
  modifyTVar counter (subtract 1)

waitGroupWait :: TVar Int -> IO ()
waitGroupWait counter = atomically do
  count <- readTVar counter
  unless (count == 0) retry

main :: IO ()
main = do
  accounts <- atomically (newArray (0, {num_accounts - 1}) 1000)
  counter <- newTVarIO 0

  replicateM_ {num_iterations} do
    source <- randomRIO (0, {num_accounts - 1})
    target <- randomRIO (0, {num_accounts - 1})
    amount <- randomRIO (0, {max_amount})

    waitGroupAdd counter
    forkIO do
      atomically do
        transfer accounts amount source target
      waitGroupDone counter

    waitGroupAdd counter
    forkIO do
      atomically do
        transfer accounts amount target source
      waitGroupDone counter

  waitGroupWait counter

  balances <- atomically do
    mapM (readArray accounts) [0..{num_accounts - 1}]

  putStrLn ("Total: " ++ show (sum balances))
"""
    output_file.write_text(content)


def create_go(num_accounts, num_iterations, max_amount, output_file):
    """Create parameterized Go program."""
    content = f"""package main

import (
	"fmt"
	"math/rand"
	"sync"
)

var accounts [{num_accounts}]int
var mutex sync.Mutex

func transfer(amount int, source int, target int) bool {{
	mutex.Lock()
	if accounts[source] < amount {{
	  mutex.Unlock()
		return false
	}}
	accounts[source] = accounts[source] - amount
	accounts[target] = accounts[target] + amount
	mutex.Unlock()
	return true
}}

func main() {{
	for i := range accounts {{
		accounts[i] = 1000
	}}

	var wg sync.WaitGroup

	for i:= range {num_iterations} {{
		random := rand.New(rand.NewSource(int64(i)))
		source := random.Intn(len(accounts))
		target := random.Intn(len(accounts))
		amount := random.Intn({max_amount})
		wg.Add(1)
		go func() {{
			for !transfer(amount, source, target) {{ }}
			wg.Done()
		}}()
		wg.Add(1)
		go func() {{
			for !transfer(amount, target, source) {{ }}
			wg.Done()
		}}()
	}}

	wg.Wait()

	total := 0
	for i := range accounts {{
		total = total + accounts[i]
	}}

	fmt.Printf("Total: %d\\n", total)
}}
"""
    output_file.write_text(content)


def run_in_nix(work_dir, cmd, env_name):
    """Run command in nix develop environment."""
    nix_cmd = ["nix", "develop", f"{work_dir}", "--command"] + cmd
    result = subprocess.run(nix_cmd, capture_output=True, text=True, cwd=work_dir)
    return result


def benchmark_config(accounts, iterations, max_amt, num_runs=3):
    """Benchmark one configuration."""
    temp_dir = Path(tempfile.mkdtemp(prefix="bench_"))
    try:
        haskell_file = temp_dir / "Accounts.hs"
        go_file = temp_dir / "main.go"

        create_haskell(accounts, iterations, max_amt, haskell_file)
        create_go(accounts, iterations, max_amt, go_file)

        # Compile Haskell in nix env
        haskell_exec = temp_dir / "Accounts"
        compile_cmd = [
            "ghc",
            "-threaded",
            "-O2",
            "-o",
            str(haskell_exec),
            str(haskell_file),
        ]
        result = run_in_nix(SCRIPT_DIR, compile_cmd, "haskell")
        if result.returncode != 0:
            print(f"Haskell compile failed: {result.stderr}")
            return None, None

        # Compile Go in nix env
        go_exec = temp_dir / "main"
        compile_cmd = ["go", "build", "-o", str(go_exec), str(go_file)]
        result = run_in_nix(GO_DIR, compile_cmd, "go")
        if result.returncode != 0:
            print(f"Go compile failed: {result.stderr}")
            return None, None

        # Run benchmarks
        haskell_times = []
        go_times = []

        for i in range(num_runs):
            # Run Haskell
            start = time.perf_counter()
            result = run_in_nix(SCRIPT_DIR, [str(haskell_exec)], "haskell")
            elapsed = time.perf_counter() - start
            if result.returncode == 0:
                haskell_times.append(elapsed)
                print(f"  Haskell run {i + 1}: {elapsed:.3f}s")

            # Run Go
            start = time.perf_counter()
            result = run_in_nix(GO_DIR, [str(go_exec)], "go")
            elapsed = time.perf_counter() - start
            if result.returncode == 0:
                go_times.append(elapsed)
                print(f"  Go run {i + 1}: {elapsed:.3f}s")

        h_mean = statistics.mean(haskell_times) if haskell_times else None
        g_mean = statistics.mean(go_times) if go_times else None
        return h_mean, g_mean
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def main():
    """Main function."""
    print("Benchmarking Haskell STM vs Go Locks...")

    configs = [
        (5, 50_000),  # Very high contention
        (10, 10_000),  # High contention
        (100, 100_000),  # Medium contention
        (10_000, 1_000_000),  # Low contention
        (100_000, 1_000_000),  # Very low contention
    ]

    results = []
    max_amt = 1000
    for accounts, iterations in configs:
        print(f"\nTesting {accounts} accounts, {iterations} iterations...")
        h_time, g_time = benchmark_config(accounts, iterations, max_amt, num_runs=3)

        if h_time and g_time:
            if h_time < g_time:
                faster = "Haskell"
                speedup = g_time / h_time
            else:
                faster = "Go"
                speedup = h_time / g_time

            results.append(
                {
                    "accounts": accounts,
                    "iterations": iterations,
                    "haskell_time": f"{h_time:.3f}",
                    "go_time": f"{g_time:.3f}",
                    "speedup": f"{speedup:.2f}",
                    "faster": faster,
                }
            )
            print(
                f"  Haskell: {h_time:.3f}s, Go: {g_time:.3f}s, {faster} is {speedup:.2f}x faster"
            )

    # Save CSV
    csv_file = SCRIPT_DIR / "benchmark_results.csv"
    with open(csv_file, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "accounts",
                "iterations",
                "haskell_time",
                "go_time",
                "speedup",
                "faster",
            ],
        )
        writer.writeheader()
        writer.writerows(results)
    print(f"\nResults saved to {csv_file}")

    # Plot
    try:
        import matplotlib.pyplot as plt

        # Read CSV manually
        with open(csv_file, "r") as f:
            reader = csv.DictReader(f)
            data = list(reader)

        labels = [f"{r['accounts']} acc, {r['iterations']} iter" for r in data]
        haskell_times = [float(r["haskell_time"]) for r in data]
        go_times = [float(r["go_time"]) for r in data]

        fig, ax = plt.subplots(figsize=(10, 6))
        x = range(len(labels))
        width = 0.35

        ax.bar(
            [i - width / 2 for i in x],
            haskell_times,
            width,
            label="Haskell STM",
            color="#5f9ea0",
        )
        ax.bar(
            [i + width / 2 for i in x],
            go_times,
            width,
            label="Go Locks",
            color="#ff7f50",
        )

        ax.set_xlabel("Configuration")
        ax.set_ylabel("Time (seconds)")
        ax.set_title("Haskell STM vs Go Locks Performance")
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=15, ha="right")
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plot_file = SCRIPT_DIR / "benchmark_plot.png"
        plt.savefig(plot_file, dpi=150)
        print(f"Plot saved to {plot_file}")
        plt.close()
    except ImportError:
        print("matplotlib not available, skipping plot")


if __name__ == "__main__":
    main()
