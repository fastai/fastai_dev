# fastai_dev

This repo is used for fastai development. fastai v2 is being developed in the `dev` folder. Docs are at http://dev.fast.ai . To install fastai v2, either use `environment.yml` to create a conda env, or:

```bash
conda install -c fastai -c pytorch jupyter "pytorch>=1.2.0" torchvision matplotlib pandas requests pyyaml fastprogress pillow
pip install typeguard jupyter_nbextensions_configurator
```

To run the tests in parallel, do something like this:

```bash
for i in {0,1,2}*.ipynb; do sleep 1; python run_notebook.py --fn $i & done
```

There are various `.py` scripts in the `dev` directory which you should look at (and we should document!)

