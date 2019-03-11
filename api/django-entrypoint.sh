#!/bin/sh
echo Running Django Migrations.
cd gsn_api
python manage.py migrate                  
python manage.py collectstatic --noinput 


echo Starting Gunicorn
gunicorn gsn_api.wsgi:application --name gsn_api --bind 127.0.0.1:8000 --workers 1 --daemon
echo Starting Envoy Reverse Proxy
cd ..
envoy -c django-service-envoy.yaml --service-cluster gsn_django


