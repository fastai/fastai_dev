#!/usr/bin/env python

# TODO: parallel

import nbformat,os
from pathlib import Path
from local.script import *
from nbconvert.preprocessors import ExecutePreprocessor

def run_nb(fn):
    nb = nbformat.read(open(fn), as_version=nbformat.NO_CONVERT)
    # TODO: filter out export cells
    print(f"Doing {fn}")
    ExecutePreprocessor(timeout=600).preprocess(nb, {})

def get_fns(path,max_num,fn):
    path = Path(path)
    if fn: return path.glob(fn)
    fns = list(path.glob("*.ipynb"))
    return [f for f in fns if f.name<max_num and not f.name.startswith('_')]

@call_parse
def main(path:Param("Path to notebooks",str)=".", max_num:Param("Max numbered notebook to run",str)=999,
         fn:Param("Filename glob",str)=None):
    "Executes notebooks in `path` and shows any exceptions. Useful for testing"
    fns = get_fns(path,max_num,fn)
    os.environ['IN_TEST']='1'
    for f in sorted(fns): run_nb(f)

