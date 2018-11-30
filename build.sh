#!/bin/bash
set -ev

echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
IMAGE_NAME=$DOCKER_USERNAME/gupy-build-cache:$TRAVIS_BRANCH

docker image build -t $IMAGE_NAME --cache-from $IMAGE_NAME src
[[ "$(docker ps -a | grep gupy-container)" ]] && docker container rm -f gupy-container
docker container run --name gupy-container $IMAGE_NAME

mkdir build
# copy the firmware
docker container cp gupy-container:/src/gupy/build/firmware.hex build/
# copy to build/tmp all py/mpy files
docker container cp gupy-container:/src/tmp/ build/
# update cache image on docker hub
docker image push $IMAGE_NAME

tar -cvzf build/$(cat $TRAVIS_BUILD_DIR/integration/tag)-mpy-modules.tar.gz build/tmp/*.mpy
tar -cvzf build/$(cat $TRAVIS_BUILD_DIR/integration/tag)-py-modules.tar.gz build/tmp/*.py
mv build/firmware.hex build/$(cat $TRAVIS_BUILD_DIR/integration/tag)-gb-firmware.hex
