"Script to generate notebooks and update html"
from fastai.gen_doc.gen_notebooks import *
import fire

if __name__ == '__main__': fire.Fire(update_notebooks)
