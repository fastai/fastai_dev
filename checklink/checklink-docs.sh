#!/bin/bash

# check links and anchors of docs.fast.ai
# throttle to 2-sec per request

echo "This will take a few minutes, it will be silent unless problems are found"

./fastai-checklink --depth 50 --quiet --broken -e --sleep 2 --timeout 60 --connection-cache 3 --exclude github.com --exclude test.pypi.org --exclude ycombinator.com --exclude anaconda.org --exclude google.com --cookies cookies.txt  https://docs.fast.ai | tee checklink-docs.log

# the script will give no output if all is good, so let's give a clear indication of success
if [[ ! -s checklink-docs.log ]]; then echo "No broken links were found"; fi
