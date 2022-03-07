# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2022 Caleb Buahin
#
# Licensed under the terms of the GNU GPLv3 License
# See LICENSE for details
# -----------------------------------------------------------------------------
"""Python setup.py installer script."""

# Standard library imports
import ast
import os
import sys

# Third party imports
from setuptools import find_packages, setup

HERE = os.path.abspath(os.path.dirname(__file__))


def get_version(module='swmmtonetcdf'):
    """Get version."""
    with open(os.path.join(HERE, module, '__init__.py'), 'r') as f:
        data = f.read()
    lines = data.split('\n')
    for line in lines:
        if line.startswith('VERSION_INFO'):
            version_tuple = ast.literal_eval(line.split('=')[-1].strip())
            version = '.'.join(map(str, version_tuple))
            break
    return version


def get_description():
    """Get long description."""
    with open(os.path.join(HERE, 'README.rst'), 'r') as f:
        data = f.read()
    return data


REQUIREMENTS = [
    'six',
    'h5py~=3.1.0',
    'netCDF4~=1.5.6',
    'cftime~=1.4.1',
    'julian~=0.14',
    'swmm-toolkit~=0.8.2',
    'numpy'
]


setup(
    name='swmmtonetcdf',
    version=get_version(),
    description='A tool to write SWMM output to netcdf',
    long_description=get_description(),
    url='https://github.com/cbuahin/swmmtonetcdf',
    author='Caleb A. Buahin',
    author_email='caleb.buahin@gmail.com',
    install_requires=REQUIREMENTS,
    packages=find_packages(exclude=['contrib', 'docs']),
    package_data={
        '': []
    },
    entry_points={
        'console_scripts': [
            'swmmtonetcdf = swmmtonetcdf.main:main'
        ]
    },
    include_package_data=True,
    license="GNU GPLv3",
    keywords="swmm5, swmm, hydraulics, hydrology, modeling, collection system",
    classifiers=[
        "Topic :: Scientific/Engineering",
        "Topic :: Documentation :: Sphinx",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: C",
        "Development Status :: 4 - Beta",
    ])
