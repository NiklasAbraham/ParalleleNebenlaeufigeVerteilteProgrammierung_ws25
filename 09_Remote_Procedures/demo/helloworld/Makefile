.PHONY: all java go python

all: java go python

java:
	mkdir -p java/src/main/java
	protoc --java_out=java/src/main/java --grpc-java_out=java/src/main/java greeter.proto
go:
	mkdir -p go
	protoc --go_out=go --go-grpc_out=go greeter.proto

python:
	mkdir -p python
	python -m grpc_tools.protoc -I. --python_out=python --grpc_python_out=python greeter.proto
