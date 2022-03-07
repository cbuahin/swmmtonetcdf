from swmmtonetcdf.tests.data import TRIVIAL_OUTPUT
from swmmtonetcdf import create_netcdf_from_swmm

import netCDF4 as nc

def test_output_save():
    netcdf_output_file = TRIVIAL_OUTPUT.replace('.out', '.nc')
    create_netcdf_from_swmm(TRIVIAL_OUTPUT, netcdf_output_file)

    ncfile = nc.Dataset(filename=netcdf_output_file, mode='r')


    # Read netcdf file and compare results
