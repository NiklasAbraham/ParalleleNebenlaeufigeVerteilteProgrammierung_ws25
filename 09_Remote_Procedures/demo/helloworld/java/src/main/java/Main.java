package greeter;

import io.grpc.Server;
import io.grpc.ServerBuilder;
import io.grpc.stub.StreamObserver;
import static greeter.Greeter.*;

public class Main {

    public static void main(String[] args) throws Exception {
        Server server = ServerBuilder.forPort(50052).addService(new SayerImpl()).build();
        server.start();
        System.out.println("Server started on :50052");
        server.awaitTermination();
    }

    static class SayerImpl extends SayerGrpc.SayerImplBase {
        @Override
        public void sayHello(HelloRequest request, StreamObserver<HelloReply> responseObserver) {
            try { Thread.sleep(0); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
            HelloReply reply = HelloReply.newBuilder().setMessage("Hello " + request.getName() + "!").build();
            responseObserver.onNext(reply);
            responseObserver.onCompleted();
        }
    }
}
