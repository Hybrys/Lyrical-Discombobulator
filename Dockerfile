# syntax=docker/dockerfile:1

FROM python:3.10.4-slim-buster

WORKDIR /app

# Set an ENV to let the app check where it is, to pick DB URI
ENV CONTAINER_DB=True

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY *.json .
COPY ./server/index.html ./server/index.html
COPY ./scraper/*.py ./scraper/
COPY ./db/*.py ./db/
COPY ./tests/*.py ./tests/
COPY ./server/*.py ./server/

CMD ["python3", "./server/main.py"]