#!/usr/bin/env python3
from local.notebook.export import script2notebook
from os import environ
from local.core.script import *

@call_parse
def main(
    folder:Param("The folder where the library is", str)="local"
):
    script2notebook(folder)
