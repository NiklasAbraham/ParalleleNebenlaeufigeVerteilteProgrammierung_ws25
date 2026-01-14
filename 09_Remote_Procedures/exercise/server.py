from concurrent import futures

import grpc
import uppercase_pb2
import uppercase_pb2_grpc


class UppercaserService(uppercase_pb2_grpc.UppercaserServicer):
    def ToUpper(self, request, context):
        """Convert the input text to uppercase."""
        return uppercase_pb2.TextReply(text=request.text.upper())


def serve(port=50051):
    """Start the gRPC server."""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    uppercase_pb2_grpc.add_UppercaserServicer_to_server(UppercaserService(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"Server started on port {port}")
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.stop(0)


if __name__ == "__main__":
    serve()
