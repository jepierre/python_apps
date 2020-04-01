# -*- coding: utf-8 -*-
# empty setup file for now


from setuptools import setup, find_packages
import setuptools

with open("README.md", "r") as f:
    readme = f.read()


with open('LICENSE') as f: 
    license = f.read()

setup(
    name='samplemodule',
    version='0.0.1',
    long_description=readme,
    author='Jean-Elie Pierre',
    license=license,
    packages=find_packages(exclude=('docs', 'tests')),
    python_requires='>3.7',
    )


