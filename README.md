# fastai_dev

This repo is used for fastai development. fastai v2 is being developed in the `dev` folder. Docs are at http://dev.fast.ai . To install fastai v2:

1. Clone this repository

```bash
git clone https://github.com/fastai/fastai_dev.git
```
2. Install packages:

```bash
conda install -c fastai -c pytorch jupyter "pytorch>=1.2.0" torchvision matplotlib pandas requests pyyaml fastprogress pillow pip scikit-learn scipy spacy
```
Alternatively, install packages using conda environment:

```bash
cd fastai_dev
conda env create -f environment.yml
```

## Tests

To run the tests in parallel, do something like this:

```bash
for i in {0,1,2}*.ipynb; do sleep 1; python run_notebook.py --fn $i & done
```

## Contributing

After you clone this repository, please run `tools/run-after-git-clone` in your terminal. This sets up git hooks, which clean up the notebooks to remove the extraneous stuff stored in the notebooks (e.g. which cells you ran) which causes unnecessary merge conflicts.

Before submitting a PR, check that the local library and notebooks match. The script `diff_nb_script.py` can let you know if there is a difference between the local library and the notebooks.
* If you made a change to the notebooks in one of the exported cells, you can export it to the library with `notebook2script.py`.
* If you made a change to the library, you can export it back to the notebooks with `script2notebook.py`.
