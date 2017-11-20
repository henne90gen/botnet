# Use an official Python runtime as a parent image
FROM python:3.6

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

STOPSIGNAL SIGTERM
