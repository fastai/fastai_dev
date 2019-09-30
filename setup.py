#!/usr/bin/env python

from setuptools import setup,find_packages

exec(open('dev/local/version.py').read())
with open('README.md') as readme_file: readme = readme_file.read()

requirements = """
    torch>=1.2.0 torchvision matplotlib pandas requests pyyaml fastprogress pillow scikit-learn scipy spacy
""".split()

setup_requirements = ['setuptools>=36.2']

setup(
    name = 'fastai2',
    version = __version__,
    packages = find_packages(),
    include_package_data = True,

    install_requires = requirements,
    setup_requires   = setup_requirements,
    python_requires  = '>=3.6',

    description = "fastai v2",
    long_description = readme,
    long_description_content_type = 'text/markdown',
    keywords = 'fastai, deep learning, machine learning',
    license = "Apache Software License 2.0",
    url = 'https://github.com/fastai/fastai_dev',
    author = "Jeremy Howard, Sylvain Gugger, and contributors",
    author_email = 'info@fast.ai',

    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    zip_safe = False,
)
