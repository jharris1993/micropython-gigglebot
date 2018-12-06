#!/bin/bash
set -ev

function sanitize() {
   local s="${1?need a string}" # receive input in first argument
   s="${s//[^[:alnum:]]/-}"     # replace all non-alnum characters to -
   s="${s//+(-)/-}"             # convert multiple - to single -
   s="${s/#-}"                  # remove - from start
   s="${s/%-}"                  # remove - from end
   echo "${s,,}"                # convert to lowercase
}

function docker_tag_exists() {
    curl --silent -f -lSL https://index.docker.io/v1/repositories/$1/tags/$2 > /dev/null
}

SANITIZED_BRANCH=$(sanitize $TRAVIS_BRANCH)

echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
IMAGE_NAME=$DOCKER_USERNAME/gupy-build-cache:$SANITIZED_BRANCH
# IMAGE_NAME=gupy-build-cache:$SANITIZED_BRANCH

if docker_tag_exists $DOCKER_USERNAME/gupy-build-cache $SANITIZED_BRANCH; then
    docker image pull $IMAGE_NAME
fi

docker image build --cache-from $IMAGE_NAME -t $IMAGE_NAME src
[[ "$(docker ps -a | grep gupy-container)" ]] && docker container rm -f gupy-container
docker container run --name gupy-container $IMAGE_NAME

mkdir build
# copy the firmware
docker container cp gupy-container:/src/gupy/build/firmware.hex build/
# copy to build/tmp all py/mpy files
docker container cp gupy-container:/src/tmp/ build/

# update cache image on docker hub
docker image push $IMAGE_NAME

pushd build
tar -cvzf $(cat $TRAVIS_BUILD_DIR/integration/tag)-mpy-modules.tar.gz tmp/*.mpy
tar -cvzf $(cat $TRAVIS_BUILD_DIR/integration/tag)-py-modules.tar.gz tmp/*.py
mv tmp/*.tar.gz $TRAVIS_BUILD_DIR/build
mv firmware.hex "(cat $TRAVIS_BUILD_DIR/integration/tag)-dexterindustries-gb-firmware.hex
popd