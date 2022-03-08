from swmmtonetcdf.swmmtonetcdf import *
from swmmtonetcdf.__main__ import main

VERSION_INFO = (0, 0, 1)

__version__ = '.'.join(map(str, VERSION_INFO))
__author__ = 'Caleb Buahin and Jenn Wu'
__copyright__ = 'Copyright (c) 2022 Caleb A. Buahin'
__licence__ = 'GNU GPLv3'
__all__ = [create_netcdf_from_swmm, main]
