#!/bin/bash
# Generate Python code from proto files

python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. uppercase.proto

echo "Generated uppercase_pb2.py and uppercase_pb2_grpc.py"
