#!/bin/bash
set -ev

docker image build -t gupy .
[ ! "$(docker ps -a | grep gupy-container)" ] && docker container rm -f gupy-container
docker container run --name gupy-container gupy

mkdir build
docker container cp gupy-container:/src/gupy/build/firmware.hex build/
docker container cp gupy-container:/src/tmp/ build/