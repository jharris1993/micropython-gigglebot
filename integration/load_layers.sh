#!/bin/bash

set -ev

if [[ -n "$(find $HOME/docker -maxdepth 0 -type d -empty 2>/dev/null)" ]]; then
    echo "docker cache non-existent"
elif [[ -d $HOME/docker ]]; then
    echo "found docker cache"
    ls $HOME/docker/*.tar.gz | xargs -I {file} bash -c "zcat {file} | docker load || exit 1";
fi

