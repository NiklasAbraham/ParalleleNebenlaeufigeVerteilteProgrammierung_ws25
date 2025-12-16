#!/usr/bin/env python3
"""Benchmark Elixir Actors vs Go Channels for Prime Sieve. Save results to CSV and plot."""

import csv
import shutil
import statistics
import subprocess
import tempfile
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.absolute()
GO_DIR = SCRIPT_DIR.parent.parent / "05_Channels" / "exercise" / "primes"
JAVA_DIR = SCRIPT_DIR.parent.parent / "03_Tasks" / "exercise"


def is_prime(n):
    """Check if n is prime."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def largest_prime_le(n):
    """Find the largest prime less than or equal to n."""
    for i in range(n, 1, -1):
        if is_prime(i):
            return i
    return None


def create_elixir(n, output_file):
    """Create parameterized Elixir program."""
    content = f"""defmodule Primes do

  def generate(n, pid) do
    for i <- 2..n do
      send(pid, {{:number, i}})
    end
    send(pid, :done)
  end

  def sieve() do
    receive do
      {{:number, prime}} ->
        IO.puts(prime)
        next = spawn(fn -> Primes.filter(prime) end)
        sieve_loop(next)
      :done ->
        :ok
    end
  end

  def sieve_loop(next) do
    receive do
      {{:number, n}} ->
        send(next, {{:number, n}})
        sieve_loop(next)
      :done ->
        send(next, :done)
        :ok
    end
  end

  def filter(prime) do
    receive do
      {{:number, n}} ->
        if rem(n, prime) != 0 do
          IO.puts(n)
          next = spawn(fn -> Primes.filter(n) end)
          filter_loop(prime, next)
        else
          filter(prime)
        end
      :done ->
        :ok
    end
  end

  def filter_loop(prime, next) do
    receive do
      {{:number, n}} ->
        if rem(n, prime) != 0 do
          send(next, {{:number, n}})
        end
        filter_loop(prime, next)
      :done ->
        send(next, :done)
        :ok
    end
  end
end

n = {n}
first = spawn(fn -> Primes.sieve() end)
Primes.generate(n, first)

# Keep process alive to allow all actors to finish processing
# For larger n, this needs to be much longer to ensure all primes are printed
Process.sleep(max(5000, div(n, 2)))
"""
    output_file.write_text(content)


def create_go(n, output_file):
    """Create parameterized Go program."""
    content = f"""package main

import (
	"fmt"
	"time"
)

func generate(n int, channel chan<- int) {{
	for i := 2; i <= n; i++ {{
		channel <- i
	}}
	close(channel)
}}

func filter(prime int, input <-chan int, output chan<- int) {{
	for n := range input {{
		if n%prime != 0 {{
			output <- n
		}}
	}}
	close(output)
}}

func main() {{
	n := {n}

	start := time.Now()

	input := make(chan int)
	go generate(n, input)

	for {{
		prime, ok := <-input
		if !ok {{
			break 
		}}

		next := make(chan int)
		go filter(prime, input, next)
		input = next 
	}}

	fmt.Printf("Sieved up to %d in %s\\n", n, time.Since(start))
}}
"""
    output_file.write_text(content)


def create_java(n, output_file):
    """Create parameterized Java program."""
    content = f"""import java.util.concurrent.*;
import java.util.Optional;

public class Primes {{
    static void generate(int n, BlockingQueue<Optional<Integer>> queue) {{
        try {{
            for (int i = 2; i <= n; i++) {{
                queue.put(Optional.of(i));
            }}
            queue.put(Optional.empty());
        }} catch (InterruptedException e) {{
        }}
    }}

    static void filter(int prime, BlockingQueue<Optional<Integer>> input, BlockingQueue<Optional<Integer>> output) {{
        try {{
            while (true) {{
                Optional<Integer> item = input.take();
                if (item.isEmpty()) {{
                    output.put(Optional.empty());
                    break;
                }}
                int num = item.get();
                if (num % prime != 0) {{
                    output.put(Optional.of(num));
                }}
            }}
        }} catch (InterruptedException e) {{
        }}
    }}

    public static void main(String[] args) throws Exception {{
        final int n = {n};
        long start = System.nanoTime();

        BlockingQueue<Optional<Integer>> input = new LinkedBlockingQueue<>();
        var executor = Executors.newVirtualThreadPerTaskExecutor();
        final BlockingQueue<Optional<Integer>> inputForLambda = input;
        executor.execute(() -> generate(n, inputForLambda));

        while (true) {{
            Optional<Integer> primeOpt = input.take();
            if (primeOpt.isEmpty()) {{
                break;
            }}
            final int prime = primeOpt.get();

            BlockingQueue<Optional<Integer>> next = new LinkedBlockingQueue<>();
            final BlockingQueue<Optional<Integer>> currentInput = input;
            final BlockingQueue<Optional<Integer>> currentOutput = next;
            executor.execute(() -> filter(prime, currentInput, currentOutput));
            input = next;
        }}

        executor.shutdown();
        boolean terminated = executor.awaitTermination(60, TimeUnit.SECONDS);
        if (!terminated) {{
            executor.shutdownNow();
        }}

        long elapsed = System.nanoTime() - start;
        System.out.printf("Sieved up to %d in %.3f ms%n", n, elapsed / 1_000_000.0);
        System.out.flush();
    }}
}}
"""
    output_file.write_text(content)


def run_in_nix(work_dir, cmd, cwd=None):
    """Run command in nix develop environment."""
    nix_cmd = ["nix", "develop", f"{work_dir}", "--command"] + cmd
    # Use provided cwd or work_dir
    actual_cwd = cwd if cwd is not None else work_dir
    # Convert Path objects to strings for subprocess
    if isinstance(actual_cwd, Path):
        actual_cwd = str(actual_cwd)
    result = subprocess.run(nix_cmd, capture_output=True, text=True, cwd=actual_cwd)
    return result


def run_elixir_watch_output(elixir_file, target_prime):
    """Run Elixir program and watch for target prime in output."""
    nix_cmd = [
        "nix",
        "develop",
        str(SCRIPT_DIR),
        "--command",
        "elixir",
        str(elixir_file),
    ]

    start_time = time.perf_counter()
    time_when_found = None

    process = subprocess.Popen(
        nix_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1
    )

    try:
        # Read lines until we find the target or process ends
        while True:
            # Read a line from stdout
            line = process.stdout.readline()
            if not line:
                # EOF reached, check if process finished
                if process.poll() is not None:
                    # Process finished, read any remaining output from buffer
                    remaining = process.stdout.read()
                    if remaining:
                        for rem_line in remaining.split("\n"):
                            rem_line = rem_line.strip()
                            if rem_line.isdigit():
                                prime = int(rem_line)
                                if prime == target_prime:
                                    time_when_found = time.perf_counter() - start_time
                                    break
                break

            line = line.strip()
            if line.isdigit():
                prime = int(line)
                if prime == target_prime:
                    time_when_found = time.perf_counter() - start_time
                    # Found it! Kill the process
                    process.terminate()
                    break

        # Wait for process to finish (with timeout)
        if process.poll() is None:
            try:
                process.wait(timeout=600)
            except subprocess.TimeoutExpired:
                process.kill()

        # Check for errors
        if process.returncode != 0 and process.returncode is not None:
            stderr_output = process.stderr.read()
            if stderr_output:
                print(f"    Elixir stderr: {stderr_output[:200]}")

    except Exception as e:
        process.kill()
        raise e

    return time_when_found


def extract_time_from_output(output):
    """Extract time in milliseconds or seconds from program output."""
    import re

    # Look for "Sieved up to X in Y" pattern in any line
    for line in output.split("\n"):
        if "Sieved up to" in line:
            # Go format: "Sieved up to 10000 in 123.456ms" or "Sieved up to 10000 in 1.234s"
            # Try seconds first (e.g., "1.234s" or "123ms")
            go_seconds = re.search(r"in ([\d.]+)s\s*$", line)
            if go_seconds:
                return float(go_seconds.group(1))

            # Try milliseconds (e.g., "123.456ms")
            go_ms = re.search(r"in ([\d.]+)ms\s*$", line)
            if go_ms:
                return float(go_ms.group(1)) / 1000.0

            # Java/Elixir format: "Sieved up to 10000 in 123.456 ms"
            # Pattern for "in X.XXX ms" (with space before ms)
            ms_match = re.search(r"in ([\d.]+)\s+ms", line)
            if ms_match:
                return float(ms_match.group(1)) / 1000.0  # Convert ms to seconds

            # Pattern for "in X.XXXms" (no space, less common)
            ms_match2 = re.search(r"in ([\d.]+)ms", line)
            if ms_match2:
                return float(ms_match2.group(1)) / 1000.0
    return None


def benchmark_config(n, num_runs=10):
    """Benchmark one configuration."""
    temp_dir = Path(tempfile.mkdtemp(prefix="bench_primes_"))
    try:
        elixir_file = temp_dir / "primes.exs"
        go_file = temp_dir / "main.go"
        java_file = temp_dir / "Primes.java"

        create_elixir(n, elixir_file)
        create_go(n, go_file)
        create_java(n, java_file)

        # Compile Java first (before any runs)
        # Use nix shell instead of nix develop to avoid shellHook issues
        java_file_abs = str(java_file.absolute())

        # Try nix shell with jdk
        compile_cmd = ["nix", "shell", "nixpkgs#jdk", "-c", "javac", java_file_abs]
        result = subprocess.run(
            compile_cmd, capture_output=True, text=True, cwd=str(temp_dir)
        )

        # Check if class file exists
        java_class = temp_dir / "Primes.class"
        if not java_class.exists() or result.returncode != 0:
            print(f"Java compile failed. Return: {result.returncode}")
            print(f"Stderr: {result.stderr[:300]}")
            print("Skipping Java benchmark - compilation failed")
            return (None, 0.0), (None, 0.0), (None, 0.0)

        # Run benchmarks
        elixir_times = []
        go_times = []
        java_times = []

        # Find the target prime (largest prime <= n)
        target_prime = largest_prime_le(n)
        if target_prime is None:
            print(f"No prime <= {n}, skipping")
            return (None, 0.0), (None, 0.0), (None, 0.0)

        print(f"  Target prime (largest <= {n}): {target_prime}")

        for i in range(num_runs):
            # Run Elixir - watch for target prime
            elapsed = run_elixir_watch_output(elixir_file, target_prime)
            if elapsed is not None:
                elixir_times.append(elapsed)
                print(
                    f"  Elixir run {i + 1}: {elapsed:.3f}s (found prime {target_prime})"
                )
            else:
                print(f"  Elixir run {i + 1} failed: target prime not found")

            # Run Go
            start = time.perf_counter()
            result = run_in_nix(GO_DIR, ["go", "run", str(go_file)])
            elapsed = time.perf_counter() - start

            if result.returncode == 0:
                # Try to extract time from output, otherwise use wall clock time
                extracted_time = extract_time_from_output(result.stdout)
                if extracted_time is not None:
                    go_times.append(extracted_time)
                    print(f"  Go run {i + 1}: {extracted_time:.3f}s (from output)")
                else:
                    go_times.append(elapsed)
                    print(f"  Go run {i + 1}: {elapsed:.3f}s (wall clock)")
            else:
                print(f"  Go run {i + 1} failed: {result.stderr}")

            # Run Java (already compiled) - use nix shell for consistency
            start = time.perf_counter()
            run_cmd = [
                "nix",
                "shell",
                "nixpkgs#jdk",
                "-c",
                "java",
                "-cp",
                str(temp_dir),
                "Primes",
            ]
            result = subprocess.run(
                run_cmd, capture_output=True, text=True, cwd=str(temp_dir)
            )
            elapsed = time.perf_counter() - start

            if result.returncode == 0:
                # Try to extract time from output, otherwise use wall clock time
                extracted_time = extract_time_from_output(result.stdout)
                if extracted_time is not None:
                    java_times.append(extracted_time)
                    print(f"  Java run {i + 1}: {extracted_time:.3f}s (from output)")
                else:
                    # Debug: show what we got
                    if result.stdout.strip():
                        print(
                            f"  Java run {i + 1}: Could not parse output. Last line: {repr(result.stdout.split(chr(10))[-2] if len(result.stdout.split(chr(10))) > 1 else result.stdout.strip())}"
                        )
                    java_times.append(elapsed)
                    print(f"  Java run {i + 1}: {elapsed:.3f}s (wall clock)")
            else:
                print(f"  Java run {i + 1} failed: {result.stderr}")

        e_mean = statistics.mean(elixir_times) if elixir_times else None
        g_mean = statistics.mean(go_times) if go_times else None
        j_mean = statistics.mean(java_times) if java_times else None

        e_std = statistics.stdev(elixir_times) if len(elixir_times) > 1 else 0.0
        g_std = statistics.stdev(go_times) if len(go_times) > 1 else 0.0
        j_std = statistics.stdev(java_times) if len(java_times) > 1 else 0.0

        return (e_mean, e_std), (g_mean, g_std), (j_mean, j_std)
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def main():
    """Main function."""
    print(
        "Benchmarking Elixir Actors vs Go Channels vs Java BlockingQueues for Prime Sieve..."
    )

    # Test different values of n (upper limit for prime sieving)
    configs = [
        100,
        1000,
        10_000,  # Small
        50_000,  # Medium-small
        100_000,  # Medium
        500_000,  # Medium-large
        # 1_000_000,  # Large
    ]

    results = []
    for n in configs:
        print(f"\nTesting n = {n}...")
        (e_time, e_std), (g_time, g_std), (j_time, j_std) = benchmark_config(
            n, num_runs=3
        )

        if e_time and g_time:
            # Java is optional - include it if available
            # Find fastest (Java optional)
            times = {"Elixir": e_time, "Go": g_time}
            if j_time:
                times["Java"] = j_time
            fastest = min(times, key=times.get)
            fastest_time = times[fastest]

            result_row = {
                "n": n,
                "elixir_time": f"{e_time:.3f}",
                "elixir_std": f"{e_std:.3f}",
                "go_time": f"{g_time:.3f}",
                "go_std": f"{g_std:.3f}",
                "java_time": f"{j_time:.3f}" if j_time else "",
                "java_std": f"{j_std:.3f}" if j_time else "",
                "fastest": fastest,
            }
            results.append(result_row)

            if j_time:
                print(
                    f"  Elixir: {e_time:.3f}s ± {e_std:.3f}s, Go: {g_time:.3f}s ± {g_std:.3f}s, Java: {j_time:.3f}s ± {j_std:.3f}s"
                )
            else:
                print(
                    f"  Elixir: {e_time:.3f}s ± {e_std:.3f}s, Go: {g_time:.3f}s ± {g_std:.3f}s, Java: skipped"
                )
            print(f"  Fastest: {fastest} ({fastest_time:.3f}s)")

    # Save CSV
    csv_file = SCRIPT_DIR / "primes_benchmark_results.csv"
    with open(csv_file, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "n",
                "elixir_time",
                "elixir_std",
                "go_time",
                "go_std",
                "java_time",
                "java_std",
                "fastest",
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

        if not data:
            print("No data to plot")
            return

        n_values = [int(r["n"]) for r in data]
        elixir_times = [float(r["elixir_time"]) for r in data]
        elixir_stds = [float(r["elixir_std"]) for r in data]
        go_times = [float(r["go_time"]) for r in data]
        go_stds = [float(r["go_std"]) for r in data]
        # Java is optional
        java_times = [
            float(r["java_time"]) if r.get("java_time") else None for r in data
        ]
        java_stds = [float(r["java_std"]) if r.get("java_std") else 0.0 for r in data]
        has_java = any(jt is not None for jt in java_times)

        fig, ax = plt.subplots(figsize=(12, 6))
        x = range(len(n_values))
        width = 0.25

        ax.bar(
            [i - width for i in x],
            elixir_times,
            width,
            yerr=elixir_stds,
            label="Elixir Actors",
            color="#5f9ea0",
            capsize=3,
        )
        ax.bar(
            x,
            go_times,
            width,
            yerr=go_stds,
            label="Go Channels",
            color="#ff7f50",
            capsize=3,
        )
        if has_java:
            ax.bar(
                [i + width for i in x],
                [jt if jt is not None else 0 for jt in java_times],
                width,
                yerr=[
                    java_stds[i] if java_times[i] is not None else 0
                    for i in range(len(java_times))
                ],
                label="Java BlockingQueues",
                color="#90ee90",
                capsize=3,
            )

        # Add fastest labels above bars
        for i, (e_time, g_time) in enumerate(zip(elixir_times, go_times)):
            j_time = (
                java_times[i]
                if i < len(java_times) and java_times[i] is not None
                else 0
            )
            max_time = max(e_time, g_time, j_time) if j_time else max(e_time, g_time)
            fastest = data[i]["fastest"]
            ax.text(
                i,
                max_time + max_time * 0.05,
                fastest,
                ha="center",
                va="bottom",
                fontsize=9,
                fontweight="bold",
            )

        ax.set_xlabel("n (upper limit)")
        ax.set_ylabel("Time (seconds)")
        ax.set_title(
            "Elixir Actors vs Go Channels vs Java BlockingQueues: Prime Sieve Performance"
        )
        ax.set_xticks(x)
        ax.set_xticklabels([f"{n:,}" for n in n_values], rotation=15, ha="right")
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plot_file = SCRIPT_DIR / "primes_benchmark_plot.png"
        plt.savefig(plot_file, dpi=150)
        print(f"Plot saved to {plot_file}")
        plt.close()

        # Create second plot with log scale
        fig, ax = plt.subplots(figsize=(12, 6))

        # Use log scale for both axes
        ax.set_xscale("log")
        ax.set_yscale("log")

        # Plot lines for each implementation
        ax.plot(
            n_values,
            elixir_times,
            marker="o",
            label="Elixir Actors",
            color="#5f9ea0",
            linewidth=2,
            markersize=6,
        )
        ax.plot(
            n_values,
            go_times,
            marker="s",
            label="Go Channels",
            color="#ff7f50",
            linewidth=2,
            markersize=6,
        )
        if has_java:
            ax.plot(
                n_values,
                [jt if jt is not None else None for jt in java_times],
                marker="^",
                label="Java BlockingQueues",
                color="#90ee90",
                linewidth=2,
                markersize=6,
            )

        ax.set_xlabel("n (upper limit, log scale)")
        ax.set_ylabel("Time (seconds, log scale)")
        ax.set_title("Prime Sieve Performance Comparison (Log-Log Scale)")
        ax.legend()
        ax.grid(True, alpha=0.3, which="both")

        plt.tight_layout()
        log_plot_file = SCRIPT_DIR / "primes_benchmark_plot_log.png"
        plt.savefig(log_plot_file, dpi=150)
        print(f"Log-scale plot saved to {log_plot_file}")
        plt.close()
    except ImportError:
        print("matplotlib not available, skipping plot")


if __name__ == "__main__":
    main()
