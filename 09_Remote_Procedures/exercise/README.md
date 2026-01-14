# Exercise 09: Remote Procedures

## Benchmark Remote Calls

Compare the performance of a gRPC call against a local function call for the same
operation: converting a string to uppercase. Use a language of your choice and
implement a gRPC service with a single method that takes a string and returns it
uppercased. Measure the latency of both the remote call and an equivalent local
function call.

Experiment with different string sizes. Document your findings.

Use files `uppercase.proto` and `benchmark.py` as starting points.

## Chat Engine

Implement a chat engine service that responds to messages with a random reply
from a predefined list of responses. The engine should implement the `Chat`
service defined in `chat.proto`.

Generate the stubs from the protocol buffer file, then implement the engine server
in a language of your choice (Python, Go, Java, etc.).

We provide a client `client.py` that you can run with:
```
python client.py
```
The client connects to `localhost:50051` and allows you to chat with the engine.

## Chat Server

Implement a chat server that sits between the client and the engine in a
language of your choice. The server receives messages from the client and
forwards them to the engine, then returns the engine's response back to the
client. Both the server and the engine implement the `Chat` service defined in
`chat.proto`.

Configure appropriate timeouts for the server's calls to the engine. Implement
retry logic to handle transient engine failures. The server should handle all
faults of the engine gracefully: network latency, crash-stop, crash-reboot, etc.
Be prepared to have your server tested against a chaos engine in the lab.

Optional Challenge: Test your implementation by introducing faults in the
engine, for example crashes and delays, and observe how the server handles them.

