#!/bin/sh

# check links and anchors of docs.fast.ai
# throttle to 2-sec per request

./fastai-checklink --depth 50 --quiet --broken -e --sleep 2 --timeout 60 --connection-cache 3 --exclude github.com --exclude test.pypi.org --exclude ycombinator.com --exclude anaconda.org --exclude google.com --cookies cookies.txt  https://docs.fast.ai | tee checklink-docs.log

# https://docs-dev.fast.ai
# multiple --location
