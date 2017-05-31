"""Custom command-line argument parser for benchmike
    Procedures:
    parse
    validate_args
"""
from argparse import ArgumentParser
from os.path import isfile

from benchmike import exceptions as err

DEFAULT_TIMEOUT = 30
DEFAULT_TIME_FILE = 'time_source.py'
DEFAULT_SIZE_FILE = 'size_source.py'
DEFAULT_STEP = 100
DEFAULT_INIT_SIZE = 100
DEFAULT_STEPS_COUNT = 100


def parse():
    """Parse args using argparse and return them as dict"""
    parser = ArgumentParser(
        description="BenchMike - tool for estimating time complexity of code")
    parser.add_argument(dest='code',
                        type=str,
                        help='path to .py file with code to be processed')
    parser.add_argument('-t',
                        dest='timeout',
                        type=int,
                        help='timeout in seconds',
                        default=DEFAULT_TIMEOUT,
                        required=False)
    parser.add_argument('--timefile',
                        dest='timefile',
                        type=str,
                        help='file where time(problem size) will be saved',
                        default=DEFAULT_TIME_FILE,
                        required=False)
    parser.add_argument('--sizefile',
                        dest='sizefile',
                        type=str,
                        help='file where max_size(time) will be saved',
                        default=DEFAULT_SIZE_FILE,
                        required=False)
    parser.add_argument('--step',
                        dest='step',
                        type=int,
                        help='step for calculations',
                        default=DEFAULT_STEP,
                        required=False)
    parser.add_argument('--start',
                        dest='start',
                        type=int,
                        help='initial size of problem',
                        default=DEFAULT_INIT_SIZE,
                        required=False)
    parser.add_argument('--count',
                        dest='count',
                        type=int,
                        help='number of steps',
                        default=DEFAULT_STEPS_COUNT,
                        required=False)
    args = vars(parser.parse_args())
    return args.get('code'), args.get('timeout'), args.get(
        'timefile'), args.get('sizefile'), args.get('step'), args.get(
        'start'), args.get('count')


def validate_args(code_path, timeout, timefile_path, sizefile_path, *args):
    """Validate values/types of arguments"""
    if not isfile(code_path):
        raise err.InvalidArgumentError('Invalid code path')
    if timeout < 0:
        raise err.InvalidArgumentError('Timeout is a negative number')
    if timefile_path != DEFAULT_TIME_FILE and not isfile(
            timefile_path):
        raise err.InvalidArgumentError('Invalid path for result file')
    if sizefile_path != DEFAULT_SIZE_FILE and not isfile(
            sizefile_path):
        raise err.InvalidArgumentError('Invalid path for result file')


if __name__ == "__main__":
    print("This is benchmike argparser")
