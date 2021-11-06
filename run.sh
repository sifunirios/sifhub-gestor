#!/bin/sh

python manage.py collectstatic --noinput
python manage.py migrate
gunicorn project.wsgi --bind=0.0.0.0:80
