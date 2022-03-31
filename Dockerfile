# syntax=docker/dockerfile:1

FROM python:3.10.4-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY *.json .
COPY index.html index.html
COPY *.py .

RUN ls -la

CMD ["python3", "main.py"]