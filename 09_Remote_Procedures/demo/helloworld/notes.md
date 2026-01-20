if rand.Float64() < 0.5 {
    return nil, status.Error(codes.Internal, "random failure")
}

if (new Random().nextDouble() < 0.5) {
    responseObserver.onError(Status.INTERNAL.withDescription("random failure").asRuntimeException());
    return;
}

