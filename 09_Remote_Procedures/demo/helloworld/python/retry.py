import grpc
from greeter_pb2 import HelloRequest
from greeter_pb2_grpc import AskerStub

service_config = """{
    "methodConfig": [{
        "name": [{"service": "helloworld.Greeter"}],
        "retryPolicy": {
            "maxAttempts": 5,
            "initialBackoff": "0.1s",
            "maxBackoff": "10s",
            "backoffMultiplier": 2,
            "retryableStatusCodes": ["UNAVAILABLE", "DEADLINE_EXCEEDED"]
        }
    }]
}"""

asker_channel = grpc.insecure_channel(
    'localhost:50051',
    options=[('grpc.service_config', service_config)]
)
asker_stub = AskerStub(asker_channel)

try:
    response = asker_stub.AskHello(
        HelloRequest(name="World"),
        timeout=20.0
    )
    print("Asker replied:", response.message)
except grpc.RpcError as e:
    print(f"Status: {e.code()}, Details: {e.details()}")

