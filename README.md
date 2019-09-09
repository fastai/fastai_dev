# fastai_dev

This repo is used for fastai development. fastai v2 is being developed in the `dev` folder. Docs are at http://dev.fast.ai . To install fastai v2:

1. Clone this repository

```bash
git clone https://github.com/fastai/fastai_dev.git
```
2. Install packages:

```bash
conda install -c fastai -c pytorch jupyter "pytorch>=1.2.0" torchvision matplotlib pandas requests pyyaml fastprogress pillow "python>=3.6" pip scikit-learn scipy spacy
pip install typeguard jupyter_nbextensions_configurator
```
Alternatively, install packages using conda environment:

```bash
cd fastai_dev
conda env create -f environment.yml
```

To run the tests in parallel, do something like this:

```bash
for i in {0,1,2}*.ipynb; do sleep 1; python run_notebook.py --fn $i & done
```

There are various `.py` scripts in the `dev` directory which you should look at (and we should document!)

