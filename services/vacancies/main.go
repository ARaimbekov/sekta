package main

import (
	"io/ioutil"
	"log"
	"net"
)

var (
	logoImg, vacanciesImg []byte
)

func init() {
	var err error
	logoImg, err = ioutil.ReadFile("logo_img.txt")
	if err != nil {
		log.Fatal(err)
	}

	vacanciesImg, err = ioutil.ReadFile("vacancies_img.txt")
	if err != nil {
		log.Fatal(err)
	}
}

func main() {
	log.Print("Start server")

	ln, err := net.Listen("tcp", ":8080")
	if err != nil {
		log.Fatal(err)
	}

	for {
		conn, err := ln.Accept()
		if err != nil {
			log.Print(err)
		}
		go handle(conn)
	}

}
