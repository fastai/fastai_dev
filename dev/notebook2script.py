#!/usr/bin/env python3
from local.notebook.export import notebook2script
from os import environ
from fastai.script import *

@call_parse
def main(
    fname:Param("A notebook name to convert", str)=None, 
    all_fs:Param("Use True for all notebooks or a glob pattern")=None,
    up_to:Param("Use to limit the conversion", str)=None 
):
    if fname is None and all_fs is None: all_fs=True
    notebook2script(fname=fname, all_fs=all_fs, up_to=up_to)
