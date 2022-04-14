#!/usr/bin/env/python3
"""module gendiff"""
import argparse

from gendiff import diff, parce, read_file
from gendiff.formatters import plain, stylish, to_json


def generate_diff(first_file, second_file, format_='stylish'):
    """
    Еhe function prints to the screen the difference between two files
    in different formats.
    Arg:
        first_file: str
        second_file: str
        format_: str

    Returns:
        str
    """
    data_first_file = read_file.read(first_file)
    data_second_file = read_file.read(second_file)
    diffs = diff.get_diff(data_first_file, data_second_file)
    if format_ == 'plain':
        print(plain.formatter(diffs))
        return plain.formatter(diffs)
    if format_ == 'json':
        print(to_json.formatter(diffs))
        return to_json.formatter(diffs)
    print(stylish.formatter(diffs))
    return stylish.formatter(diffs)


def main():
    args = parce.parce_file()
    generate_diff(args.first_file, args.second_file, args.format)


if __name__ == '__main__':
    main()
