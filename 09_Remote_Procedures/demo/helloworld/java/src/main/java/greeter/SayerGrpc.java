package greeter;

import static io.grpc.MethodDescriptor.generateFullMethodName;

/**
 */
@io.grpc.stub.annotations.GrpcGenerated
public final class SayerGrpc {

  private SayerGrpc() {}

  public static final java.lang.String SERVICE_NAME = "greeter.Sayer";

  // Static method descriptors that strictly reflect the proto.
  private static volatile io.grpc.MethodDescriptor<greeter.Greeter.HelloRequest,
      greeter.Greeter.HelloReply> getSayHelloMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "SayHello",
      requestType = greeter.Greeter.HelloRequest.class,
      responseType = greeter.Greeter.HelloReply.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<greeter.Greeter.HelloRequest,
      greeter.Greeter.HelloReply> getSayHelloMethod() {
    io.grpc.MethodDescriptor<greeter.Greeter.HelloRequest, greeter.Greeter.HelloReply> getSayHelloMethod;
    if ((getSayHelloMethod = SayerGrpc.getSayHelloMethod) == null) {
      synchronized (SayerGrpc.class) {
        if ((getSayHelloMethod = SayerGrpc.getSayHelloMethod) == null) {
          SayerGrpc.getSayHelloMethod = getSayHelloMethod =
              io.grpc.MethodDescriptor.<greeter.Greeter.HelloRequest, greeter.Greeter.HelloReply>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "SayHello"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  greeter.Greeter.HelloRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  greeter.Greeter.HelloReply.getDefaultInstance()))
              .setSchemaDescriptor(new SayerMethodDescriptorSupplier("SayHello"))
              .build();
        }
      }
    }
    return getSayHelloMethod;
  }

  /**
   * Creates a new async stub that supports all call types for the service
   */
  public static SayerStub newStub(io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<SayerStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<SayerStub>() {
        @java.lang.Override
        public SayerStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new SayerStub(channel, callOptions);
        }
      };
    return SayerStub.newStub(factory, channel);
  }

  /**
   * Creates a new blocking-style stub that supports all types of calls on the service
   */
  public static SayerBlockingV2Stub newBlockingV2Stub(
      io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<SayerBlockingV2Stub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<SayerBlockingV2Stub>() {
        @java.lang.Override
        public SayerBlockingV2Stub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new SayerBlockingV2Stub(channel, callOptions);
        }
      };
    return SayerBlockingV2Stub.newStub(factory, channel);
  }

  /**
   * Creates a new blocking-style stub that supports unary and streaming output calls on the service
   */
  public static SayerBlockingStub newBlockingStub(
      io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<SayerBlockingStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<SayerBlockingStub>() {
        @java.lang.Override
        public SayerBlockingStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new SayerBlockingStub(channel, callOptions);
        }
      };
    return SayerBlockingStub.newStub(factory, channel);
  }

  /**
   * Creates a new ListenableFuture-style stub that supports unary calls on the service
   */
  public static SayerFutureStub newFutureStub(
      io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<SayerFutureStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<SayerFutureStub>() {
        @java.lang.Override
        public SayerFutureStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new SayerFutureStub(channel, callOptions);
        }
      };
    return SayerFutureStub.newStub(factory, channel);
  }

  /**
   */
  public interface AsyncService {

    /**
     */
    default void sayHello(greeter.Greeter.HelloRequest request,
        io.grpc.stub.StreamObserver<greeter.Greeter.HelloReply> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getSayHelloMethod(), responseObserver);
    }
  }

  /**
   * Base class for the server implementation of the service Sayer.
   */
  public static abstract class SayerImplBase
      implements io.grpc.BindableService, AsyncService {

    @java.lang.Override public final io.grpc.ServerServiceDefinition bindService() {
      return SayerGrpc.bindService(this);
    }
  }

  /**
   * A stub to allow clients to do asynchronous rpc calls to service Sayer.
   */
  public static final class SayerStub
      extends io.grpc.stub.AbstractAsyncStub<SayerStub> {
    private SayerStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected SayerStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new SayerStub(channel, callOptions);
    }

    /**
     */
    public void sayHello(greeter.Greeter.HelloRequest request,
        io.grpc.stub.StreamObserver<greeter.Greeter.HelloReply> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getSayHelloMethod(), getCallOptions()), request, responseObserver);
    }
  }

  /**
   * A stub to allow clients to do synchronous rpc calls to service Sayer.
   */
  public static final class SayerBlockingV2Stub
      extends io.grpc.stub.AbstractBlockingStub<SayerBlockingV2Stub> {
    private SayerBlockingV2Stub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected SayerBlockingV2Stub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new SayerBlockingV2Stub(channel, callOptions);
    }

    /**
     */
    public greeter.Greeter.HelloReply sayHello(greeter.Greeter.HelloRequest request) throws io.grpc.StatusException {
      return io.grpc.stub.ClientCalls.blockingV2UnaryCall(
          getChannel(), getSayHelloMethod(), getCallOptions(), request);
    }
  }

  /**
   * A stub to allow clients to do limited synchronous rpc calls to service Sayer.
   */
  public static final class SayerBlockingStub
      extends io.grpc.stub.AbstractBlockingStub<SayerBlockingStub> {
    private SayerBlockingStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected SayerBlockingStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new SayerBlockingStub(channel, callOptions);
    }

    /**
     */
    public greeter.Greeter.HelloReply sayHello(greeter.Greeter.HelloRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getSayHelloMethod(), getCallOptions(), request);
    }
  }

  /**
   * A stub to allow clients to do ListenableFuture-style rpc calls to service Sayer.
   */
  public static final class SayerFutureStub
      extends io.grpc.stub.AbstractFutureStub<SayerFutureStub> {
    private SayerFutureStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected SayerFutureStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new SayerFutureStub(channel, callOptions);
    }

    /**
     */
    public com.google.common.util.concurrent.ListenableFuture<greeter.Greeter.HelloReply> sayHello(
        greeter.Greeter.HelloRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getSayHelloMethod(), getCallOptions()), request);
    }
  }

  private static final int METHODID_SAY_HELLO = 0;

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
        case METHODID_SAY_HELLO:
          serviceImpl.sayHello((greeter.Greeter.HelloRequest) request,
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
          getSayHelloMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              greeter.Greeter.HelloRequest,
              greeter.Greeter.HelloReply>(
                service, METHODID_SAY_HELLO)))
        .build();
  }

  private static abstract class SayerBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoFileDescriptorSupplier, io.grpc.protobuf.ProtoServiceDescriptorSupplier {
    SayerBaseDescriptorSupplier() {}

    @java.lang.Override
    public com.google.protobuf.Descriptors.FileDescriptor getFileDescriptor() {
      return greeter.Greeter.getDescriptor();
    }

    @java.lang.Override
    public com.google.protobuf.Descriptors.ServiceDescriptor getServiceDescriptor() {
      return getFileDescriptor().findServiceByName("Sayer");
    }
  }

  private static final class SayerFileDescriptorSupplier
      extends SayerBaseDescriptorSupplier {
    SayerFileDescriptorSupplier() {}
  }

  private static final class SayerMethodDescriptorSupplier
      extends SayerBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoMethodDescriptorSupplier {
    private final java.lang.String methodName;

    SayerMethodDescriptorSupplier(java.lang.String methodName) {
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
      synchronized (SayerGrpc.class) {
        result = serviceDescriptor;
        if (result == null) {
          serviceDescriptor = result = io.grpc.ServiceDescriptor.newBuilder(SERVICE_NAME)
              .setSchemaDescriptor(new SayerFileDescriptorSupplier())
              .addMethod(getSayHelloMethod())
              .build();
        }
      }
    }
    return result;
  }
}
