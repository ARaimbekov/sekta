FROM golang:1.18-alpine

WORKDIR /vacancies
COPY vendor vendor
ADD cmd/main.go .
ADD go.mod .
COPY internal internal
RUN go build -o main main.go
CMD ["./main"]