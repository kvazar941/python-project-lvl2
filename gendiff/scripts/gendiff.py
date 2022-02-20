#!/usr/bin/env/python3
"""module gendiff"""
import argparse


parser = argparse.ArgumentParser(prog='gendiff', description='Generate diff')
parser.add_argument('first_file')
parser.add_argument('second_file')
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
