#!/usr/bin/env/python3
"""module gendiff"""
import argparse


parser = argparse.ArgumentParser(description='Generate diff')
parser.add_argument('first_file')
parser.add_argument('second_file')
parser.add_argument('-f', '--format', help='set format of output')
args = parser.parse_args()

def main():
    """
    main code

    Returns:
        str
    """
    return 'Hello!'


if __name__ == '__main__':
    main()
