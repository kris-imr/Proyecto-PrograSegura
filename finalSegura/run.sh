#!/bin/bash

sleep 15

python manage.py makemigrations
python manage.py migrate


#python manage.py runserver 0.0.0.0:8080
gunicorn --bind :8000 finalSegura6.wsgi:application --reload