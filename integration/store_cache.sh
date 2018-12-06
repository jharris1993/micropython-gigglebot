#!/bin/bash
set -ev

IMAGE_LIST="$(docker image ls -aq)"

if [[ $TRAVIS_EVENT_TYPE == cron || $TRAVIS_EVENT_TYPE == api ]]; then 
    rm -rf $HOME/docker
elif [[ -n "$IMAGE_LIST" ]]; then
    mkdir -p $HOME/docker
    for layer in $IMAGE_LIST; do
        echo "storing layer $layer as cache in $HOME/docker"
        if [[ ! -e $HOME/docker/$layer.tar.gz ]]; then
            docker save $layer | gzip -2 > $HOME/docker/$layer.tar.gz
        else
            echo "layer $layer is already cached"
        fi
    done
fi 