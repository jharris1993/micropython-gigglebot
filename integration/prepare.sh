#!/bin/bash

set -ev

if [[ $TRAVIS_EVENT_TYPE == cron ]]; then
   exit 0
fi

js-yaml $TRAVIS_BUILD_DIR/changelog.yaml > $TRAVIS_BUILD_DIR/integration/changelog.json
last_tag=$(git describe --tags --abbrev=0)

if [[ ! $last_tag ]]; then
    node $TRAVIS_BUILD_DIR/integration/release.js v0.0.0
else
    node $TRAVIS_BUILD_DIR/integration/release.js $last_tag
fi

echo "Title of new release is \"$(cat $TRAVIS_BUILD_DIR/integration/title)\""
cat $TRAVIS_BUILD_DIR/integration/changelog.md