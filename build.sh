#!/bin/bash
set -ev

if [[ $TRAVIS_EVENT_TYPE == cron ]]; then
   exit 0
fi

function sanitize() {
   local s="${1?need a string}" # receive input in first argument
   s="${s//[^[:alnum:]]/-}"     # replace all non-alnum characters to -
   s="${s//+(-)/-}"             # convert multiple - to single -
   s="${s/#-}"                  # remove - from start
   s="${s/%-}"                  # remove - from end
   echo "${s,,}"                # convert to lowercase
}

# function docker_tag_exists() {
#     curl --silent -f -lSL https://index.docker.io/v1/repositories/$1/tags/$2 > /dev/null
# }

SANITIZED_BRANCH=$(sanitize $TRAVIS_BRANCH)

# echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
# IMAGE_NAME=$DOCKER_USERNAME/gupy-build-cache:$SANITIZED_BRANCH
IMAGE_NAME=gupy-build-cache:$SANITIZED_BRANCH

# if docker_tag_exists $DOCKER_USERNAME/gupy-build-cache $SANITIZED_BRANCH; then
#     docker image pull $IMAGE_NAME
# fi

docker image build -t $IMAGE_NAME src
[[ "$(docker ps -a | grep gupy-container)" ]] && docker container rm -f gupy-container
docker container run --name gupy-container $IMAGE_NAME

mkdir build
# copy the firmware
docker container cp gupy-container:/src/gupy/build/firmware.hex build/
# copy to build/tmp all py/mpy files
docker container cp gupy-container:/src/tmp/ build/

# update cache image on docker hub
# docker image push $IMAGE_NAME

tar -cvzf build/$(cat $TRAVIS_BUILD_DIR/integration/tag)-mpy-modules.tar.gz build/tmp/*.mpy
tar -cvzf build/$(cat $TRAVIS_BUILD_DIR/integration/tag)-py-modules.tar.gz build/tmp/*.py
mv build/firmware.hex build/$(cat $TRAVIS_BUILD_DIR/integration/tag)-gb-firmware.hex
