# Use an official Python runtime as a parent image
FROM nginx:1.13

RUN apt-get update && \
    apt-get -y dist-upgrade && \
    # TODO remove nano and curl install
    apt-get -y install curl nano

WORKDIR /app

ADD . /app

COPY nginx.conf /etc/nginx/nginx.conf

# copy js and css bundles into webserver root
COPY ./bin/bundle.js /app/app/bundle.js
COPY ./bin/bundle.css /app/app/bundle.css
