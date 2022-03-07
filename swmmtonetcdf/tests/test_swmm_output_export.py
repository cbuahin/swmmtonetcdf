from swmmtonetcdf.tests.data import TRIVIAL_OUTPUT
from swmmtonetcdf import create_netcdf_from_swmm


def test_output_save():
    netcdf_output_file = TRIVIAL_OUTPUT.replace('.out', '.nc')
    create_netcdf_from_swmm(TRIVIAL_OUTPUT, netcdf_output_file)

    # Read netcdf file and compare results
