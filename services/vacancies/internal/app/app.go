package app

import (
	"fmt"
	"log"
	"net"
	"vacancies/internal/vacancy"
	"vacancies/internal/vacancy/protobuf"

	"google.golang.org/grpc"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

const (
	APP_PORT    = ":8080"
	DB_HOST     = "db"
	DB_PORT     = 5432
	DB_USER     = "postgres"
	DB_PASSWORD = "postgres"
	DB_NAME     = "postgres"
)

func Run() (err error) {
	listener, err := net.Listen("tcp", APP_PORT)
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
		DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)

	return gorm.Open(postgres.Open(dsn), &gorm.Config{})
}
