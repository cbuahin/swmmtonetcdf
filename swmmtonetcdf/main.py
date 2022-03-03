# Python imports
import os
from argparse import ArgumentParser, ArgumentError


def valid_file(parser: ArgumentParser, arg):
    if not os.path.exists(arg) or not arg or not arg.strip():
        parser.error(f'The specified file {arg} does not exist!')
        raise ArgumentError(f'The specified file {arg} does not exist!')
    else:
        return arg


def boolean(parser: ArgumentParser, arg):
    boolean_input = str(arg).lower()
    return 'yes' in boolean_input or 'y' in boolean_input or 'true' in boolean_input


def valid_path(parser: ArgumentParser, arg):
    path = os.path.dirname(arg)

    if not os.path.exists(path) or not arg or not arg.strip():
        parser.error(f'Parent folder for specified path {arg} does not exist!')
        raise ArgumentError(f'Parent folder for specified path {arg} does not exist!')
    else:
        return arg


def main():
    # Setup the command line argument parser.
    parser = ArgumentParser()

    subparsers = parser.add_subparsers(help="Sub-command help", dest='sub_parser_name')

    # Calculates diff and writes to json
    convert_command = subparsers.add_parser(name="convert", help="Converts SWMM output file to netcdf")
    convert_command.add_argument("--out", help='Path to base SWMM output file', type=lambda x: valid_file(parser, x))
    convert_command.add_argument("--nc", help='Path to NetCDF file', type=lambda x: valid_path(parser, x))
    convert_command.add_argument("--geom", help='Save geometry', action='store_true')
    convert_command.add_argument("--no-geom", help='Save geometry', action='store_true')
    convert_command.set_defaults(geom=True)
    convert_command.add_argument("--prj", help='WKT projection to use for geometry', default='EPSG:4326')

    if args.sub_parser_name.lower() == 'convert':
        convert()


def convert():
    pass


if __name__ == '__main__':
    main()
