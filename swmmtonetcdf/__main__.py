# Python imports
import os
import sys
from argparse import ArgumentParser, ArgumentError
from typing import Any

from swmmtonetcdf import create_netcdf_from_swmm

def valid_file(parser: ArgumentParser, arg: Any):
    """
    Parses filepath to ensure that file is valid and exists.

    Args:
        parser (ArgumentParser): Argument parser.
        arg (Any): Argument to parse
    Returns:
        Filepath if deemed as valid.
    """
    if not os.path.exists(arg) or not arg or not arg.strip():
        parser.error(f'The specified file {arg} does not exist!')
        raise ArgumentError(
            argument=arg,
            message=f'The specified file {arg} does not exist!'
        )
    else:
        return arg


def valid_path(parser: ArgumentParser, arg):
    """

    Args:
        parser (ArgumentParser): Argument parser.
        arg (Any): Argument to parse

    Returns:

    """
    path = os.path.dirname(arg)

    if not os.path.exists(path) or not arg or not arg.strip():
        parser.error(f'Parent folder for specified path {arg} does not exist!')
        raise ArgumentError(
            argument=arg,
            message=f'Parent folder for specified path {arg} does not exist!'
        )
    else:
        return arg


def main():
    """

    Returns:

    """
    # Setup the command line argument parser.
    parser = ArgumentParser()

    subparsers = parser.add_subparsers(help="Sub-command help", dest='sub_parser_name')

    # Calculates diff and writes to json
    convert_command = subparsers.add_parser(name="convert", help="Converts SWMM output file to netcdf")
    convert_command.add_argument("--out", help='Path to base SWMM output file', type=lambda x: valid_file(parser, x))
    convert_command.add_argument("--nc", help='Path to NetCDF file', type=lambda x: valid_path(parser, x))
    convert_command.add_argument("--inp", help='Input file to extract geometry from', action='store_true')
    convert_command.add_argument("--geom", help='Save geometry', action='store_true')
    convert_command.add_argument("--no-geom", help='Save geometry', action='store_false')
    convert_command.set_defaults(geom=True)
    convert_command.add_argument("--prj", help='WKT projection to use for geometry', default='EPSG:4326')

    args = parser.parse_args()

    if args.sub_parser_name.lower() == 'convert':
        create_netcdf_from_swmm(swmm_output_file=args.out, netcdf_output_file=args.nc)


if __name__ == '__main__':
    sys.exit(main())
