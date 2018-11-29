#!/bin/bash

set -ev

js-yaml changelog.yaml > changelog.json
last_tag=$(git describe --tags --abbrev=0)

if [[ $last_tag ]]; then
    node release.js v0.0.0
else
    node release.js $last_tag
fi

