#!/bin/bash
set -ev

if [[ $TRAVIS_EVENT_TYPE == cron || $TRAVIS_EVENT_TYPE == api ]]; then 
    rm -rf $HOME/docker
else
    mkdir -p $HOME/docker && docker images -a --format '{{.Repository}}:{{.Tag}} {{.ID}}' \
    | xargs -n 2 -t sh -c 'test -e $HOME/docker/$1.tar.gz || docker save $0 | gzip -2 > $HOME/docker/$1.tar.gz'
fi 