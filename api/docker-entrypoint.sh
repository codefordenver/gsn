#!/bin/bash
cd gsn_api
python manage.py migrate                  
python manage.py collectstatic --noinput 


# Start Gunicorn processes
echo Starting Gunicorn.
exec  gunicorn gsn_api.wsgi:application \
    --name gsn_api \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    "$@"