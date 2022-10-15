package app

import (
	"fmt"
	"log"
	"net"
	"vacancies/src/vacancy"
	"vacancies/src/vacancy/protobuf"

	"google.golang.org/grpc"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

const (
	PORT = ":8080"
)

const (
	host     = "db"
	port     = 5432
	user     = "postgres"
	password = "postgres"
	dbname   = "postgres"
)

func Run() (err error) {
	listener, err := net.Listen("tcp", PORT)
	if err != nil {
		return
	}

	db, err := NewDB()
	if err != nil {
		return
	}

	var opts []grpc.ServerOption
	server := grpc.NewServer(opts...)
	protobuf.RegisterVacanciesServer(server, vacancy.NewHandler(db))

	log.Print("run server ...")
	return server.Serve(listener)
}

func NewDB() (db *gorm.DB, err error) {
	log.Print("init db")

	dsn := fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=disable",
		host, port, user, password, dbname)

	return gorm.Open(postgres.Open(dsn), &gorm.Config{})
}
