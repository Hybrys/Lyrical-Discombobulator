# syntax=docker/dockerfile:1

FROM python:3.10.4-slim-buster

WORKDIR /app

# Set an ENV to let the app check where it is, to pick DB URI
ENV CONTAINER_DB=True

# Recommended ENV variables for dockerized apps
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install syllapy --no-deps

COPY *.json .
COPY *.py .
COPY ./discombob/* ./discombob/
COPY ./index.html ./index.html
COPY ./scraper/*.py ./scraper/
COPY ./db/*.py ./db/
COPY ./api/*.py ./api/
COPY ./tests/*.py ./tests/
COPY ./tests/mock/*.pickle ./tests/mock/

ENTRYPOINT ["gunicorn", "-w", "2", "-b", "0.0.0.0:4000", "main:app"]