#! /bin/bash

cd docker_base && docker build -t botnet_base .
docker-compose up
