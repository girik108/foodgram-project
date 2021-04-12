#!/bin/sh

set -e
#Wait Postgresql
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

#Flush DB. Collect static and migrate
python3 manage.py flush --noinput
python3 manage.py collectstatic --noinput
python3 manage.py migrate
#python3 manage.py importingredients

#Load DUMP file
DUMP_FILE="fixtures.json"

if test -f "$DUMP_FILE"; then
    echo "Load data"
    python3 manage.py loaddata fixtures.json
fi

#Create super user if env set
echo "Check SUPERUSER"
if [ "$DJANGO_SUPERUSER_USERNAME" ]
then
    python manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_EMAIL
fi

#RUN Gunicorn
gunicorn --bind 0.0.0.0:8000 foodgram.wsgi

exec "$@"