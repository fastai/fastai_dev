#!/usr/bin/env python3
from local.notebook.export import diff_nb_script
from os import environ
from local.core.script import *

@call_parse
def main(
    lib_folder:Param("The folder where the library is", str)="local"
):
    diff_nb_script(lib_folder=lib_folder)
