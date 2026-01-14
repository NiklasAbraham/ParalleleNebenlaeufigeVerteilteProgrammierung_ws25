import grpc
import time
from uppercase_pb2 import TextRequest
from uppercase_pb2_grpc import UppercaserStub

def to_upper(text):
    return text.upper()

def benchmark_local(text, iterations):
    start = time.time()
    for _ in range(iterations):
        to_upper(text)
    end = time.time()
    return (end - start) / iterations

def benchmark_grpc(stub, text, iterations):
    start = time.time()
    for _ in range(iterations):
        stub.ToUpper(TextRequest(text=text))
    end = time.time()
    return (end - start) / iterations

channel = grpc.insecure_channel('localhost:50051')
stub = UppercaserStub(channel)

sizes = [1, 10, 100, 1000]
iterations = 1000

for size in sizes:
    text = 'a' * size
    local_time = benchmark_local(text, iterations)
    grpc_time = benchmark_grpc(stub, text, iterations)
    print(f"{size} bytes: local={local_time*1000:.3f}ms, grpc={grpc_time*1000:.3f}ms")

