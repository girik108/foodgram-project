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

#Flush DB
echo "Check FLUSH DB"
if [ "$DJANGO_FLUSH_DB" ]
then
    python3 manage.py flush --noinput
    echo "DB if empty"
fi

python3 manage.py collectstatic --noinput
python3 manage.py migrate

#Load DUMP file of import
DUMP_FILE="fixtures.json"

if test -f "$DUMP_FILE"; 
then
    echo "Load data"
    python3 manage.py loaddata fixtures.json
else
    echo "Import ingredients"
    python3 manage.py importingredients
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