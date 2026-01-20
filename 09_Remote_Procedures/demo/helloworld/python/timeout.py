import grpc
from greeter_pb2 import HelloRequest
from greeter_pb2_grpc import AskerStub, SayerStub

asker_stub = AskerStub(grpc.insecure_channel('localhost:50051'))
try:
    response = asker_stub.AskHello(HelloRequest(name="World"), timeout=2.0)
    print("Asker replied:", response.message)
except grpc.RpcError as e:
    print(f"Status: {e.code()}, Details: {e.details()}")

sayer_stub = SayerStub(grpc.insecure_channel('localhost:50052'))
try:
    response = sayer_stub.SayHello(HelloRequest(name="World"), timeout=2.0)
    print("Sayer replied:", response.message)
except grpc.RpcError as e:
    print(f"Status: {e.code()}, Details: {e.details()}")

