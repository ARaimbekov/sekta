package app

import (
	"log"
	"net"
	"vacancies/database"
	"vacancies/vacancies"

	"google.golang.org/grpc"
)

const PORT = ":8080"

func Run() (err error) {

	listener, err := net.Listen("tcp", PORT)
	if err != nil {
		return
	}

	db, err := database.NewDB()
	if err != nil {
		return
	}
	defer db.Close()

	err = database.Migrate(db)
	if err != nil {
		return
	}

	var opts []grpc.ServerOption
	server := grpc.NewServer(opts...)
	vacancies.RegisterVacanciesServer(server, NewHandler(db))

	log.Print("run server ...")
	return server.Serve(listener)
}
