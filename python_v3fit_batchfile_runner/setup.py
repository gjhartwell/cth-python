# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 09:56:28 2020

@author: hartwgj
"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python_v3fit_batchfile_runner-GREG-HARTWELL", 
    version="0.0.1",
    author="Greg hartwell",
    author_email="hartwell@physics.auburn.edu",
    description="A python package to remotely perform V3FIT reconstructions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gjhartwell/cth-pythont",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)