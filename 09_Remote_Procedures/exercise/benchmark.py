import statistics
import time

import grpc
from uppercase_pb2 import TextRequest
from uppercase_pb2_grpc import UppercaserStub


def to_upper(text):
    """Local function to convert text to uppercase."""
    return text.upper()


def benchmark_local(text, iterations, warmup_iterations=100):
    """Benchmark local function call."""
    # Warmup
    for _ in range(warmup_iterations):
        to_upper(text)

    # Actual benchmark
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        to_upper(text)
        end = time.perf_counter()
        times.append((end - start) * 1000)  # Convert to milliseconds

    return {
        "mean": statistics.mean(times),
        "median": statistics.median(times),
        "min": min(times),
        "max": max(times),
        "stdev": statistics.stdev(times) if len(times) > 1 else 0.0,
    }


def benchmark_grpc(stub, text, iterations, warmup_iterations=100):
    """Benchmark gRPC remote call."""
    # Warmup
    for _ in range(warmup_iterations):
        stub.ToUpper(TextRequest(text=text))

    # Actual benchmark
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        stub.ToUpper(TextRequest(text=text))
        end = time.perf_counter()
        times.append((end - start) * 1000)  # Convert to milliseconds

    return {
        "mean": statistics.mean(times),
        "median": statistics.median(times),
        "min": min(times),
        "max": max(times),
        "stdev": statistics.stdev(times) if len(times) > 1 else 0.0,
    }


def main(
    server_address="localhost:50051", sizes=None, iterations=1000, warmup_iterations=100
):
    """Run the benchmark comparing local vs gRPC calls."""
    if sizes is None:
        sizes = [1, 10, 100, 1000, 10000, 100000, 1000000]

    print("=" * 80)
    print("Benchmark: Local Function Call vs gRPC Remote Call")
    print("=" * 80)
    print(f"Server address: {server_address}")
    print(f"Iterations per test: {iterations}")
    print(f"Warmup iterations: {warmup_iterations}")
    print("=" * 80)
    print()

    # Connect to gRPC server
    try:
        channel = grpc.insecure_channel(server_address)
        stub = UppercaserStub(channel)
        # Test connection
        stub.ToUpper(TextRequest(text="test"))
        print(f"Connected to gRPC server at {server_address}")
    except grpc.RpcError:
        print(f"Error: Could not connect to gRPC server at {server_address}")
        print("Make sure the server is running: python server.py")
        return
    except Exception as e:
        print(f"Error: {e}")
        return

    print()
    print(
        f"{'Size (bytes)':<15} {'Local Mean (ms)':<20} {'gRPC Mean (ms)':<20} {'Overhead':<15}"
    )
    print("-" * 80)

    results = []

    for size in sizes:
        text = "a" * size

        # Benchmark local call
        local_stats = benchmark_local(text, iterations, warmup_iterations)

        # Benchmark gRPC call
        grpc_stats = benchmark_grpc(stub, text, iterations, warmup_iterations)

        # Calculate overhead
        overhead = (
            (grpc_stats["mean"] - local_stats["mean"]) / local_stats["mean"]
        ) * 100

        results.append(
            {
                "size": size,
                "local": local_stats,
                "grpc": grpc_stats,
                "overhead": overhead,
            }
        )

        print(
            f"{size:<15} {local_stats['mean']:<20.3f} {grpc_stats['mean']:<20.3f} {overhead:<15.1f}%"
        )

    print()
    print("=" * 80)
    print("Detailed Statistics:")
    print("=" * 80)

    for result in results:
        print(f"\nSize: {result['size']} bytes")
        print(
            f"  Local:  mean={result['local']['mean']:.3f}ms, "
            f"median={result['local']['median']:.3f}ms, "
            f"min={result['local']['min']:.3f}ms, "
            f"max={result['local']['max']:.3f}ms, "
            f"stdev={result['local']['stdev']:.3f}ms"
        )
        print(
            f"  gRPC:   mean={result['grpc']['mean']:.3f}ms, "
            f"median={result['grpc']['median']:.3f}ms, "
            f"min={result['grpc']['min']:.3f}ms, "
            f"max={result['grpc']['max']:.3f}ms, "
            f"stdev={result['grpc']['stdev']:.3f}ms"
        )
        print(f"  Overhead: {result['overhead']:.1f}%")

    channel.close()


if __name__ == "__main__":
    main()
