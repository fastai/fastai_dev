#!/bin/bash
for nb in ./*.ipynb; do tools/sgen_notebook.py "$nb"; done
