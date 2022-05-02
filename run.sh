#!/bin/bash
sudo docker compose up -d --build
sudo docker compose exec web python manage.py collectstatic
sudo docker compose exec web python manage.py migrate
