#!/bin/bash

set -ev

js-yaml $TRAVIS_BUILD_DIR/changelog.yaml > $TRAVIS_BUILD_DIR/integration/changelog.json
last_tag=$(git describe --tags --abbrev=0)

if [[ $last_tag ]]; then
    node $TRAVIS_BUILD_DIR/integration/release.js v0.0.0
else
    node $TRAVIS_BUILD_DIR/integration/release.js $last_tag
fi

