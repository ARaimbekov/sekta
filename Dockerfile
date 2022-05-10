FROM python:3.9-slim-buster

WORKDIR /app

RUN adduser --system --home /app --shell /usr/sbin/nologin --no-create-home --disabled-password mewor

RUN apt update && apt install -y python3-dev default-libmysqlclient-dev build-essential netcat

COPY requirements.txt .

RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

COPY app .

ENTRYPOINT ["./run.sh"]
