# Exercise 09: Remote Procedures

# Commnands

```
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. uppercase.proto
```


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

================================================================================
Benchmark: Local Function Call vs gRPC Remote Call
================================================================================
Server address: localhost:50051
Iterations per test: 1000
Warmup iterations: 100
================================================================================

Connected to gRPC server at localhost:50051

Size (bytes)    Local Mean (ms)      gRPC Mean (ms)       Overhead       
--------------------------------------------------------------------------------
1               0.000                0.159                138954.5       %
10              0.000                0.180                183965.3       %
100             0.000                0.168                155735.4       %
1000            0.000                0.198                53803.7        %
10000           0.002                0.191                7885.4         %
100000          0.023                0.306                1233.8         %
1000000         0.196                3.372                1617.2         %

================================================================================
Detailed Statistics:
================================================================================

Size: 1 bytes
  Local:  mean=0.000ms, median=0.000ms, min=0.000ms, max=0.000ms, stdev=0.000ms
  gRPC:   mean=0.159ms, median=0.136ms, min=0.118ms, max=0.631ms, stdev=0.056ms
  Overhead: 138954.5%

Size: 10 bytes
  Local:  mean=0.000ms, median=0.000ms, min=0.000ms, max=0.000ms, stdev=0.000ms
  gRPC:   mean=0.180ms, median=0.188ms, min=0.103ms, max=0.546ms, stdev=0.058ms
  Overhead: 183965.3%

Size: 100 bytes
  Local:  mean=0.000ms, median=0.000ms, min=0.000ms, max=0.000ms, stdev=0.000ms
  gRPC:   mean=0.168ms, median=0.142ms, min=0.103ms, max=0.752ms, stdev=0.060ms
  Overhead: 155735.4%

Size: 1000 bytes
  Local:  mean=0.000ms, median=0.000ms, min=0.000ms, max=0.003ms, stdev=0.000ms
  gRPC:   mean=0.198ms, median=0.141ms, min=0.132ms, max=0.740ms, stdev=0.102ms
  Overhead: 53803.7%

Size: 10000 bytes
  Local:  mean=0.002ms, median=0.002ms, min=0.002ms, max=0.006ms, stdev=0.000ms
  gRPC:   mean=0.191ms, median=0.154ms, min=0.135ms, max=1.014ms, stdev=0.070ms
  Overhead: 7885.4%

Size: 100000 bytes
  Local:  mean=0.023ms, median=0.023ms, min=0.022ms, max=0.054ms, stdev=0.002ms
  gRPC:   mean=0.306ms, median=0.286ms, min=0.252ms, max=1.035ms, stdev=0.067ms
  Overhead: 1233.8%

Size: 1000000 bytes
  Local:  mean=0.196ms, median=0.190ms, min=0.190ms, max=0.253ms, stdev=0.011ms
  gRPC:   mean=3.372ms, median=3.353ms, min=2.056ms, max=5.565ms, stdev=0.518ms
  Overhead: 1617.2%


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

