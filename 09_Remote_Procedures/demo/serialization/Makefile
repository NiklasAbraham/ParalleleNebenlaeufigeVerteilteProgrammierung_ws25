.PHONY: all java go python clean

all: java go python

java:
	protoc --java_out=. types.proto

go:
	protoc --go_out=. types.proto

python:
	python -m grpc_tools.protoc -I. --python_out=. types.proto
