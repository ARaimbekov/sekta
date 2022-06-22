package main

import (
	"bufio"
	"bytes"
	"errors"
	"fmt"
	"log"
	"net"
	"os"
	"os/exec"
	"strconv"
	"strings"
)

type Vacancy struct {
	Name      string
	DemonLord string
	MinAge    int
}

var (
	chooseVacancy   = []byte("| Choose vacancy\n> ")
	whoIsDemonLord  = []byte("| Who is your demon lord?\n> ")
	whatAge         = []byte("| What is your age?\n> ")
	enterToContinue = []byte("| Press Enter to continue ...\n")
	shortPipe       = []byte("======================\n")

	tokenResult = "| Congratulations! Token: "
)

var (
	ErrNotNum         = errors.New("not a number")
	ErrOutOfRange     = errors.New("number out of vanacy range")
	ErrUnmeetCriteria = errors.New("sorry, you haven't met criteria")
)

func handle(conn net.Conn) {

	var err error

	defer printErr(err)
	defer conn.Close()

	if _, err = conn.Write(logoImg); err != nil {
		return
	}

	var vs []Vacancy
	for {

		if vs, err = scanVacancies(); err != nil {
			return
		}

		if err = printVacancies(conn, vs); err != nil {
			return
		}

		if err = processCommand(conn, vs); err != nil {
			return
		}

		if err = waitToContinue(conn); err != nil {
			return
		}
	}
}

func printErr(err error) {
	if err != nil {
		log.Print(err)
	}
}

func scanVacancies() (vs []Vacancy, err error) {
	file, err := os.Open("vacancies.txt")
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
		vs[i].DemonLord = splitedStr[1]
		vs[i].MinAge, _ = strconv.Atoi(splitedStr[2])
	}

	vs = vs[:i]
	err = scanner.Err()
	return
}

func printVacancies(conn net.Conn, vs []Vacancy) (err error) {

	if _, err = conn.Write(vacanciesImg); err != nil {
		return
	}

	for i, v := range vs {
		str := fmt.Sprintf("#%d\nName: %s\nDescription: %s\nMinimal age:%d\n\n", i, v.Name, v.DemonLord, v.MinAge)
		if _, err = conn.Write([]byte(str)); err != nil {
			return
		}
	}

	_, err = conn.Write(shortPipe)
	return
}

func processCommand(conn net.Conn, vs []Vacancy) (err error) {

	defer func() {
		if err != nil {
			errBs := []byte("| Err:" + err.Error() + "\n")
			_, err = conn.Write(errBs)
			if err != nil {
				return
			}
			err = nil
		}
	}()

	num, err := scanVacancyNum(conn, len(vs))
	if err != nil {
		return
	}

	demonLord, err := scanString(conn, whoIsDemonLord)
	if err != nil {
		return
	}

	age, err := scanString(conn, whatAge)
	if err != nil {
		return
	}

	if err = genToken(conn); err != nil {
		return
	}

	print(num)
	print(demonLord)
	print(age)

	return
}

func scanVacancyNum(conn net.Conn, maxLen int) (num int, err error) {
	if _, err = conn.Write(chooseVacancy); err != nil {
		return
	}

	numStr, err := bufio.NewReader(conn).ReadString('\n')
	if err != nil {
		return
	}
	numStr = numStr[:len(numStr)-1]

	num, err = strconv.Atoi(numStr)
	if err != nil {
		err = ErrNotNum
		return
	}

	if num >= maxLen {
		err = ErrOutOfRange
		return
	}
	return
}

func scanString(conn net.Conn, ask []byte) (str string, err error) {

	if _, err = conn.Write(ask); err != nil {
		return
	}

	str, err = bufio.NewReader(conn).ReadString('\n')
	if err != nil {
		return
	}

	return
}

func genToken(conn net.Conn) (err error) {
	cmd := exec.Command("./gen")

	var buf bytes.Buffer
	cmd.Stdout = &buf

	if err = cmd.Run(); err != nil {
		return
	}

	token := buf.String()
	if token == "" {
		err = ErrUnmeetCriteria
		return
	}

	str := tokenResult + token

	if _, err = conn.Write([]byte(str)); err != nil {
		return
	}

	return
}

func waitToContinue(conn net.Conn) (err error) {
	if _, err = conn.Write(enterToContinue); err != nil {
		return
	}

	_, err = bufio.NewReader(conn).ReadString('\n')
	if err != nil {
		return
	}

	return
}
