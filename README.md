# fastai_dev

This repo is used for fastai development. fastai v2 is being developed in the `dev` folder. Docs are at http://dev.fast.ai . 

## Install

1. Clone this repository

   `git clone https://github.com/fastai/fastai_dev.git`
   
2. Install the required packages

   ```bash
   cd fastai_dev
   conda env create -f environment.yml
   ```

## Run

1. Activate the environment

   `conda activate fastai_dev`

2. Run Jupyter Notebook

   `jupyter notebook`
   
3. Check out the notebooks in dev/ folder.

Using conda's environment is the easiest way. 
Should you object, you may install the mentioned in `environment.yml` packages by hand:

```bash
conda install -c fastai -c pytorch <conda packages list>
pip install <pip packages list>
```

## Running tests

To run the tests in parallel, do something like this:

```bash
for i in {0,1,2}*.ipynb; do sleep 1; python run_notebook.py --fn $i & done
```

There are various `.py` scripts in the `dev` directory which you should look at (and we should document!)

