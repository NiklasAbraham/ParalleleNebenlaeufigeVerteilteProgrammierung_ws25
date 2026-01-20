package main

import (
	"context"
	"log"
	"net"
	"time"

	"google.golang.org/grpc"

	pb "demo/greeter"
)

type askerServer struct {
	pb.UnimplementedAskerServer
}

func (s *askerServer) AskHello(context context.Context, request *pb.HelloRequest) (*pb.HelloReply, error) {
	time.Sleep(3000 * time.Millisecond)
	return &pb.HelloReply{
		Message: "Hello " + request.GetName() + "?",
	}, nil
}

func main() {
	listener, _ := net.Listen("tcp", ":50051")
	grpcServer := grpc.NewServer()
	pb.RegisterAskerServer(grpcServer, &askerServer{})
	log.Println("Server started on :50051")
	grpcServer.Serve(listener)
}

