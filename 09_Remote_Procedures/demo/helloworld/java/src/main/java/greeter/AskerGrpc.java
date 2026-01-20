package greeter;

import static io.grpc.MethodDescriptor.generateFullMethodName;

/**
 */
@io.grpc.stub.annotations.GrpcGenerated
public final class AskerGrpc {

  private AskerGrpc() {}

  public static final java.lang.String SERVICE_NAME = "greeter.Asker";

  // Static method descriptors that strictly reflect the proto.
  private static volatile io.grpc.MethodDescriptor<greeter.Greeter.HelloRequest,
      greeter.Greeter.HelloReply> getAskHelloMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "AskHello",
      requestType = greeter.Greeter.HelloRequest.class,
      responseType = greeter.Greeter.HelloReply.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<greeter.Greeter.HelloRequest,
      greeter.Greeter.HelloReply> getAskHelloMethod() {
    io.grpc.MethodDescriptor<greeter.Greeter.HelloRequest, greeter.Greeter.HelloReply> getAskHelloMethod;
    if ((getAskHelloMethod = AskerGrpc.getAskHelloMethod) == null) {
      synchronized (AskerGrpc.class) {
        if ((getAskHelloMethod = AskerGrpc.getAskHelloMethod) == null) {
          AskerGrpc.getAskHelloMethod = getAskHelloMethod =
              io.grpc.MethodDescriptor.<greeter.Greeter.HelloRequest, greeter.Greeter.HelloReply>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "AskHello"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  greeter.Greeter.HelloRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  greeter.Greeter.HelloReply.getDefaultInstance()))
              .setSchemaDescriptor(new AskerMethodDescriptorSupplier("AskHello"))
              .build();
        }
      }
    }
    return getAskHelloMethod;
  }

  /**
   * Creates a new async stub that supports all call types for the service
   */
  public static AskerStub newStub(io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<AskerStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<AskerStub>() {
        @java.lang.Override
        public AskerStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new AskerStub(channel, callOptions);
        }
      };
    return AskerStub.newStub(factory, channel);
  }

  /**
   * Creates a new blocking-style stub that supports all types of calls on the service
   */
  public static AskerBlockingV2Stub newBlockingV2Stub(
      io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<AskerBlockingV2Stub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<AskerBlockingV2Stub>() {
        @java.lang.Override
        public AskerBlockingV2Stub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new AskerBlockingV2Stub(channel, callOptions);
        }
      };
    return AskerBlockingV2Stub.newStub(factory, channel);
  }

  /**
   * Creates a new blocking-style stub that supports unary and streaming output calls on the service
   */
  public static AskerBlockingStub newBlockingStub(
      io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<AskerBlockingStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<AskerBlockingStub>() {
        @java.lang.Override
        public AskerBlockingStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new AskerBlockingStub(channel, callOptions);
        }
      };
    return AskerBlockingStub.newStub(factory, channel);
  }

  /**
   * Creates a new ListenableFuture-style stub that supports unary calls on the service
   */
  public static AskerFutureStub newFutureStub(
      io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<AskerFutureStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<AskerFutureStub>() {
        @java.lang.Override
        public AskerFutureStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new AskerFutureStub(channel, callOptions);
        }
      };
    return AskerFutureStub.newStub(factory, channel);
  }

  /**
   */
  public interface AsyncService {

    /**
     */
    default void askHello(greeter.Greeter.HelloRequest request,
        io.grpc.stub.StreamObserver<greeter.Greeter.HelloReply> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getAskHelloMethod(), responseObserver);
    }
  }

  /**
   * Base class for the server implementation of the service Asker.
   */
  public static abstract class AskerImplBase
      implements io.grpc.BindableService, AsyncService {

    @java.lang.Override public final io.grpc.ServerServiceDefinition bindService() {
      return AskerGrpc.bindService(this);
    }
  }

  /**
   * A stub to allow clients to do asynchronous rpc calls to service Asker.
   */
  public static final class AskerStub
      extends io.grpc.stub.AbstractAsyncStub<AskerStub> {
    private AskerStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected AskerStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new AskerStub(channel, callOptions);
    }

    /**
     */
    public void askHello(greeter.Greeter.HelloRequest request,
        io.grpc.stub.StreamObserver<greeter.Greeter.HelloReply> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getAskHelloMethod(), getCallOptions()), request, responseObserver);
    }
  }

  /**
   * A stub to allow clients to do synchronous rpc calls to service Asker.
   */
  public static final class AskerBlockingV2Stub
      extends io.grpc.stub.AbstractBlockingStub<AskerBlockingV2Stub> {
    private AskerBlockingV2Stub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected AskerBlockingV2Stub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new AskerBlockingV2Stub(channel, callOptions);
    }

    /**
     */
    public greeter.Greeter.HelloReply askHello(greeter.Greeter.HelloRequest request) throws io.grpc.StatusException {
      return io.grpc.stub.ClientCalls.blockingV2UnaryCall(
          getChannel(), getAskHelloMethod(), getCallOptions(), request);
    }
  }

  /**
   * A stub to allow clients to do limited synchronous rpc calls to service Asker.
   */
  public static final class AskerBlockingStub
      extends io.grpc.stub.AbstractBlockingStub<AskerBlockingStub> {
    private AskerBlockingStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected AskerBlockingStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new AskerBlockingStub(channel, callOptions);
    }

    /**
     */
    public greeter.Greeter.HelloReply askHello(greeter.Greeter.HelloRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getAskHelloMethod(), getCallOptions(), request);
    }
  }

  /**
   * A stub to allow clients to do ListenableFuture-style rpc calls to service Asker.
   */
  public static final class AskerFutureStub
      extends io.grpc.stub.AbstractFutureStub<AskerFutureStub> {
    private AskerFutureStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected AskerFutureStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new AskerFutureStub(channel, callOptions);
    }

    /**
     */
    public com.google.common.util.concurrent.ListenableFuture<greeter.Greeter.HelloReply> askHello(
        greeter.Greeter.HelloRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getAskHelloMethod(), getCallOptions()), request);
    }
  }

  private static final int METHODID_ASK_HELLO = 0;

  private static final class MethodHandlers<Req, Resp> implements
      io.grpc.stub.ServerCalls.UnaryMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ServerStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ClientStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.BidiStreamingMethod<Req, Resp> {
    private final AsyncService serviceImpl;
    private final int methodId;

    MethodHandlers(AsyncService serviceImpl, int methodId) {
      this.serviceImpl = serviceImpl;
      this.methodId = methodId;
    }

    @java.lang.Override
    @java.lang.SuppressWarnings("unchecked")
    public void invoke(Req request, io.grpc.stub.StreamObserver<Resp> responseObserver) {
      switch (methodId) {
        case METHODID_ASK_HELLO:
          serviceImpl.askHello((greeter.Greeter.HelloRequest) request,
              (io.grpc.stub.StreamObserver<greeter.Greeter.HelloReply>) responseObserver);
          break;
        default:
          throw new AssertionError();
      }
    }

    @java.lang.Override
    @java.lang.SuppressWarnings("unchecked")
    public io.grpc.stub.StreamObserver<Req> invoke(
        io.grpc.stub.StreamObserver<Resp> responseObserver) {
      switch (methodId) {
        default:
          throw new AssertionError();
      }
    }
  }

  public static final io.grpc.ServerServiceDefinition bindService(AsyncService service) {
    return io.grpc.ServerServiceDefinition.builder(getServiceDescriptor())
        .addMethod(
          getAskHelloMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              greeter.Greeter.HelloRequest,
              greeter.Greeter.HelloReply>(
                service, METHODID_ASK_HELLO)))
        .build();
  }

  private static abstract class AskerBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoFileDescriptorSupplier, io.grpc.protobuf.ProtoServiceDescriptorSupplier {
    AskerBaseDescriptorSupplier() {}

    @java.lang.Override
    public com.google.protobuf.Descriptors.FileDescriptor getFileDescriptor() {
      return greeter.Greeter.getDescriptor();
    }

    @java.lang.Override
    public com.google.protobuf.Descriptors.ServiceDescriptor getServiceDescriptor() {
      return getFileDescriptor().findServiceByName("Asker");
    }
  }

  private static final class AskerFileDescriptorSupplier
      extends AskerBaseDescriptorSupplier {
    AskerFileDescriptorSupplier() {}
  }

  private static final class AskerMethodDescriptorSupplier
      extends AskerBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoMethodDescriptorSupplier {
    private final java.lang.String methodName;

    AskerMethodDescriptorSupplier(java.lang.String methodName) {
      this.methodName = methodName;
    }

    @java.lang.Override
    public com.google.protobuf.Descriptors.MethodDescriptor getMethodDescriptor() {
      return getServiceDescriptor().findMethodByName(methodName);
    }
  }

  private static volatile io.grpc.ServiceDescriptor serviceDescriptor;

  public static io.grpc.ServiceDescriptor getServiceDescriptor() {
    io.grpc.ServiceDescriptor result = serviceDescriptor;
    if (result == null) {
      synchronized (AskerGrpc.class) {
        result = serviceDescriptor;
        if (result == null) {
          serviceDescriptor = result = io.grpc.ServiceDescriptor.newBuilder(SERVICE_NAME)
              .setSchemaDescriptor(new AskerFileDescriptorSupplier())
              .addMethod(getAskHelloMethod())
              .build();
        }
      }
    }
    return result;
  }
}
