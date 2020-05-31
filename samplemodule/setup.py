# -*- coding: utf-8 -*-
# empty setup file for now


from setuptools import setup, find_packages
import setuptools
from samplemodule.version import __version__

with open("README.md", "r") as f:
    readme = f.read()


with open("LICENSE") as f:
    license = f.read()

setup(
    name="samplemodule",
    version=__version__,
    long_description=readme,
    author="Jean-Elie Pierre",
    license=license,
    packages=find_packages(exclude=("docs", "tests")),
    python_requires=">3.7",
)
