FROM golang:1.18-alpine

WORKDIR /vacancies

ADD go.mod .
ADD go.sum .
RUN go mod download

COPY main.go .
COPY src ./src

RUN go build -o main

EXPOSE 8080

CMD [ "./main" ]