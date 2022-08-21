package main

import (
	"bufio"
	"context"
	"fmt"
	"io/ioutil"
	"os"
	"regexp"
	"strconv"
	"strings"
	"vacancies/vacancies"

	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

var (
	fileName    = "vacancies.txt"
	searchRegex = `(%s)\s+(\d+)\s+`
	getRegex    = `(%s)\s+(\d+)\s+([\S]+)`
	errNotFound = status.Error(codes.NotFound, "vacancy not found")
)

type (
	Vacancy struct {
		Name   string
		MinAge uint32
		Token  string
	}

	handler struct{}
)

func NewHandler() handler {
	return handler{}
}

func (h handler) List(_ context.Context, req *vacancies.ListRequest) (resp *vacancies.ListResponse, err error) {
	vs, err := scanVacancies()
	if err != nil {
		return
	}

	resp = &vacancies.ListResponse{}
	resp.Vacancies = make([]*vacancies.Vacancy, len(vs))
	for i, v := range vs {
		resp.Vacancies[i] = &vacancies.Vacancy{
			Name:   v.Name,
			MinAge: int32(v.MinAge),
		}
	}
	return
}

func (h handler) Search(_ context.Context, req *vacancies.SearchRequest) (resp *vacancies.SearchResponse, err error) {

	content, err := ioutil.ReadFile(fileName)
	if err != nil {
		return
	}

	expression := fmt.Sprintf(searchRegex, req.Name)
	x, err := regexp.Compile(expression)
	if err != nil {
		return
	}

	match := x.FindStringSubmatch(string(content))

	if len(match) < 2 {
		err = errNotFound
		return
	}

	age, _ := strconv.Atoi(match[2])

	resp = &vacancies.SearchResponse{
		Vacancy: &vacancies.Vacancy{
			Name:   match[1],
			MinAge: int32(age),
		},
	}

	return
}

func (h handler) Create(_ context.Context, req *vacancies.CreateRequest) (resp *vacancies.CreateResponse, err error) {

	f, err := os.OpenFile(fileName, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		return
	}

	defer func() {
		errClose := f.Close()
		if errClose != nil {
			err = errClose
		}
	}()

	str := fmt.Sprintf("%s %d %s\n", req.Name, req.MinAge, req.Token)

	_, err = f.WriteString(str)
	if err != nil {
		return
	}

	resp = &vacancies.CreateResponse{}

	return
}

func (h handler) Get(_ context.Context, req *vacancies.GetRequest) (resp *vacancies.GetResponse, err error) {
	content, err := ioutil.ReadFile(fileName)
	if err != nil {
		return
	}

	expression := fmt.Sprintf(getRegex, req.Name)
	x, err := regexp.Compile(expression)
	if err != nil {
		return
	}

	match := x.FindStringSubmatch(string(content))
	token := match[3]

	resp = &vacancies.GetResponse{
		Token: token,
	}

	return
}

func scanVacancies() (vs []Vacancy, err error) {
	file, err := os.Open(fileName)
	if err != nil {
		return
	}
	defer file.Close()

	var i int
	vs = make([]Vacancy, 40)
	scanner := bufio.NewScanner(file)
	for i = 0; i < 40; i++ {
		if !scanner.Scan() {
			break
		}

		splitedStr := strings.Split(scanner.Text(), " ")
		if len(splitedStr) < 3 {
			continue
		}

		vs[i].Name = splitedStr[0]
		age, _ := strconv.Atoi(splitedStr[1])
		vs[i].MinAge = uint32(age)
		vs[i].Token = splitedStr[2]
	}

	vs = vs[:i]
	err = scanner.Err()
	return
}
