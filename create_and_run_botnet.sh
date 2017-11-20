#! /bin/bash

# build base image for bots
cd docker_base && \
docker build -t botnet_base . && \
cd ..

cd frontend && \
sh build_container.sh

docker-compose up $1
