# swmmtonetcdf
A python package for converting swmm output to netcdf

## PyPi Deployment Instructions

1. Install required packages for deployment to pypi
`pip install --upgrade build`
`pip install twine`

2. Build codebase and upload to pypi 
`python -m build`
`python -m twine upload swmmtonetcdf dist/*`