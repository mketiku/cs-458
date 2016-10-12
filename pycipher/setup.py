#!/usr/bin/env python
from setuptools import setup, find_packages


setup(
    name='pycipher',
    version='0.5.2',
    description='Several simple cipher algorithms',
    packages=find_packages(exclude=['tests','tests.*']),
    include_package_data=True,  # declarations in MANIFEST.in
    test_suite='tests',

)
