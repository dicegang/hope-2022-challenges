FROM golang:1.18-buster AS builder

WORKDIR /app

COPY go.* ./
RUN go mod download

COPY *.go ./
RUN go build -o ./server

FROM debian:buster-slim

WORKDIR /app
COPY flag.txt /app/
COPY --from=builder /app/server /app/

EXPOSE 8081
ENTRYPOINT [ "/app/server" ]
