package main

import (
	"log"
	"net"
	"vacancies/vacancies"

	"google.golang.org/grpc"
)

func main() {

	listener, err := net.Listen("tcp", ":8080")
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}

	var opts []grpc.ServerOption

	grpcServer := grpc.NewServer(opts...)
	vacancies.RegisterVacanciesServer(grpcServer, NewHandler())

	log.Print("vacancies started ...")
	err = grpcServer.Serve(listener)
	log.Print(err)
}
