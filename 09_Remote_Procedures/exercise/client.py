import grpc
from chat_pb2 import MessageRequest
from chat_pb2_grpc import ChatStub

channel = grpc.insecure_channel('localhost:50051')
stub = ChatStub(channel)

while True:
    text = input("> ")
    if not text:
        break
    response = stub.SendMessage(MessageRequest(text=text))
    print(response.text)

