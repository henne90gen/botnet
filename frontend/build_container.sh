#!/usr/bin/env bash

npm install && \
npm run build && \
docker build -t botnet_frontend .