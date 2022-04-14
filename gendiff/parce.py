"""module parce."""
import argparse

HELP = 'set format of output'


def parce_file():
    """
    Create a parser with the necessary arguments for the application to work.

    Returns:
        parser
    """
    parser = argparse.ArgumentParser(description='Generate diff')
    parser.add_argument('-f', '--format', default='stylish', help=HELP)
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    return parser.parse_args()
