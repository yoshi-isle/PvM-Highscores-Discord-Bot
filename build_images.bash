#!/bin/bash

source config/local.env

docker build \
  . \
  --build-arg=BOT_TOKEN=$BOT_TOKEN \
  --build-arg=MONGODB_CONNECTION_STRING=$MONGODB_CONNECTION_STRING \
  --build-arg=WOM_TOKEN=$WOM_TOKEN \
  --build-arg=CLIENT_ID=$CLIENT_ID \
  --build-arg=CLIENT_SECRET=$CLIENT_SECRET \
  --build-arg=ACCESS_TOKEN=$ACCESS_TOKEN \
  --build-arg=REFRESH_TOKEN=$REFRESH_TOKEN \
  --network=host \
  -t bot:latest