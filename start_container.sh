#!/bin/sh
echo "Build Container"
docker build -t bitstarter:latest  .
echo "Run Container"
docker run --name bitstarter -v $PWD:/app:rw -p 8000:8000 --rm bitstarter:latest
