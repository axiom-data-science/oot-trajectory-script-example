#!python
import logging
from pathlib import Path

import pandas as pd
from pocean.dsg import IncompleteMultidimensionalTrajectory

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__file__)


def make_trajectory_netcdf(input_file, nc_file, axes):
    """Given input file with specified axes, write CF-compliant incomplete trajectory file

    args:
    - input_file (str) - input file path
    - nc_file (str) - output file path
    - axes (dir) - dir that maps columns to axes (e.g. {'trajectory': 'particle_id', 'time': 'time', 'x': 'lon', 'y': 'lat', 'z': depth})
    """
    df = pd.read_csv(input_file, parse_dates=[axes['t']])
    logger.info(f'read {input_file}')

    IncompleteMultidimensionalTrajectory.from_dataframe(df, nc_file, axes=axes)
    logger.info(f'created {nc_file}')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=str, help='file to convert to trajectory file')
    parser.add_argument('nc_file', type=str, help='output ncfile')
    parser.add_argument('--trajectory', type=str, default='trajectory', help='trajectory id')
    parser.add_argument('--time', type=str, default='time', help='time column name')
    parser.add_argument('--lat', type=str, default='lat', help='lat column name')
    parser.add_argument('--lon', type=str, default='lon', help='lon column name')
    parser.add_argument('--depth', type=str, default='depth', help='depth column name')
    args = parser.parse_args()

    input_file = Path(args.input_file)
    if not input_file.exists():
        parser.error(f'{input_file} does not exist')

    nc_file = Path(args.nc_file)
    out_dir = nc_file.parent
    if not out_dir.exists():
        out_dir.mkdir(parents=True)
        logger.info(f'created {out_dir}')

    axes = {
        'trajectory': args.trajectory,
        't': args.time,
        'x': args.lon,
        'y': args.lat,
        'z': args.depth
    }
    make_trajectory_netcdf(input_file, nc_file, axes)
