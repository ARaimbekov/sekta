FROM golang:1.18-alpine

RUN apk update && \
    apk add build-base

RUN mkdir /app 
COPY . /app
WORKDIR /app
RUN go build -o server . 

CMD [ "/app/server" ]