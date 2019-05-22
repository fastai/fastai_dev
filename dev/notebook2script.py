#!/usr/bin/env python3
from fastai_local.notebook.export import notebook2script
from fastai.script import *

@call_parse
def main(
    fname:Param("A notebook name to convert", str), 
    up_to:Param("Use to limit the conversion", str),
    all_fs:Param("Use True for all notebooks or a glob pattern")=True, 
):
    notebook2script(fname=fname, all_fs=all_fs, up_to=up_to)
