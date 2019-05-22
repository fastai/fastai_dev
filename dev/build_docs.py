#!/usr/bin/env python3
from fastai_local.notebook.export2html import convert_all
from fastai.script import *

@call_parse
def main(
    force_all:Param("A notebook name to convert", bool)=False
):
    convert_all(force_all=force_all)