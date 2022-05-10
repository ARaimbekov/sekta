#!/bin/sh

until nc -z -v -w30 mysql 3306
do
  echo "Waiting for database connection..."
  sleep 1
done

python3 manage.py makemigrations main
python3 manage.py migrate --noinput
python3 manage.py runserver 0.0.0.0:8080 --insecure
