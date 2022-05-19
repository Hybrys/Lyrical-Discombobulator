# syntax=docker/dockerfile:1

FROM python:3.10.4-slim-buster

WORKDIR /app

# Set an ENV to let the app check where it is, to pick DB URI
ENV CONTAINER_DB=True

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

CMD ["python3", "./main.py"]