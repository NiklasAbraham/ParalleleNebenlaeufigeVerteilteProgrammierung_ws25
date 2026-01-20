import grpc
from greeter_pb2 import HelloRequest
from greeter_pb2_grpc import AskerStub, SayerStub

asker_channel = grpc.insecure_channel('localhost:50051')
asker_stub = AskerStub(asker_channel)

response = asker_stub.AskHello(HelloRequest(name="World"))
print("Asker replied:", response.message)
response = asker_stub.AskHello(HelloRequest(name="World"))
print("Asker replied:", response.message)




sayer_channel = grpc.insecure_channel('localhost:50052')
sayer_stub = SayerStub(sayer_channel)

response = sayer_stub.SayHello(HelloRequest(name="World"))
print("Sayer replied:", response.message)



