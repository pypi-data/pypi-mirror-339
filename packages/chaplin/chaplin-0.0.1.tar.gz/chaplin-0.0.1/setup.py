#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
     name='chaplin',
     zip_safe=False,
     include_package_data=True,

     version='0.0.1',

     author="Gabriele Orlando",

     author_email="gabriele.orlando@kuleuven.be",

     description="A predictor of protein-chaperon interaction",

     long_description=long_description,

     long_description_content_type="text/markdown",

     url="https://github.com/grogdrinker/chaplin",
     
     packages=['chaplin',"chaplin.src"],
     package_dir={'chaplin': 'chaplin/','chaplin.src': 'chaplin/src/'},
     package_data={'chaplin': ['marshalled/*','marshalled/final_modelBert.hugg_m/*']},
     
     scripts=['chaplin_standalone'],


     install_requires=["torch","numpy", "scikit-learn","transformers"],

     classifiers=[

         "Programming Language :: Python :: 3",

         "Operating System :: OS Independent",

     ],

 )
