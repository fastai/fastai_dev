# fastai_docs
Documentation source for fastai (see http://docs.fast.ai for final docs)

If you want to help us and contribute to the docs, you just have to make modifications to the corresponding source notebook(s) under `docs_src/`, our scripts will then automatically convert them to HTML.

Beforehand, please execute the following instructions to ensure that everything works properly.
```
git clone https://github.com/fastai/fastai_docs
cd fastai_docs
tools/run-after-git-clone
```
The last line on Windows should be replaced by
```
python tools\run-after-git-clone
```
The [documentation](http://docs.fast.ai/gen_doc.html#Process-for-contributing-to-the-docs) goes more in depth about all the functionalities the `gen_doc` module offers, but if you just want to add a sentence or correct a typo, make a PR with the notebook changed and we'll take care of the rest.
