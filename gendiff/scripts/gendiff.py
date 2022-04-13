#!/usr/bin/env/python3
"""module gendiff"""
import argparse
from gendiff import parce, diff, read_file
from gendiff.formatters import stylish, plain, to_json


def generate_diff(first_file, second_file, format_='stylish'):
    """
    Еhe function prints to the screen the difference between two files 
    in different formats

    Returns:
        str
    """
    diffs = diff.get_diff(read_file.read(first_file), read_file.read(second_file))
    if format_ == 'plain':
        print(plain.formatter(diffs))
        return plain.formatter(diffs)
    elif format_ == 'json':
        print(to_json.formatter(diffs))
        return to_json.formatter(diffs)
    else:
        print(stylish.formatter(diffs))
        return stylish.formatter(diffs)


def main():
    args = parce.parce_file()
    generate_diff(args.first_file, args.second_file, args.format)

if __name__ == '__main__':
    main()

