# pull official base image
FROM python:3.8

RUN apt-get update && apt-get install -y netcat

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

# install dependencies
RUN mkdir /app

COPY requirements.txt /app

WORKDIR /app

RUN pip install -r requirements.txt

# copy project
COPY . .

# run entrypoint
RUN ["chmod", "+x", "/app/entrypoint.sh"]
ENTRYPOINT ["/app/entrypoint.sh"]