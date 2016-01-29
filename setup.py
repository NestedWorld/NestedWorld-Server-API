#!/usr/bin/env python
from setuptools import setup, find_packages

REQUIREMENTS = [line.strip() for line in open('requirements.txt')]

setup(
    name='nestedworld_api',
    version='0.1.0',

    install_requires=REQUIREMENTS,
    packages=find_packages(),
)
