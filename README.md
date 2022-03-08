# swmmtonetcdf

A python package for converting swmm output to netcdf.

## Project Information

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

[![Build Test](https://github.com/cbuahin/swmmtonetcdf/actions/workflows/commit.yml/badge.svg)](https://github.com/cbuahin/swmmtonetcdf/actions)

[![Build Test and Deploy](https://github.com/cbuahin/swmmtonetcdf/actions/workflows/deploy.yml/badge.svg)](https://github.com/cbuahin/swmmtonetcdf/actions)

## PyPi Deployment Instructions

1. Install required packages for deployment to pypi  
`pip install --upgrade build`  
`pip install twine`  

2. Build codebase and upload to pypi  
`python -m build`  
`python -m twine upload swmmtonetcdf dist/*`  

## PyPI Deployment via Github Action
Make a tagged release