#!/bin/bash

# make sure spacy's en default model is installed before tests are run
python -c 'import spacy; spacy.load("en")' 2>1 >> /dev/null || python -m spacy download en

python -m pytest -p nbval "$@"
