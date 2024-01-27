#!/bin/bash

source config/local.env

docker build . --build-arg=BOT_TOKEN=$BOT_TOKEN  --build-arg=MONGODB_CONNECTION_STRING=$MONGODB_CONNECTION_STRING --network=host -t bot:latest  
