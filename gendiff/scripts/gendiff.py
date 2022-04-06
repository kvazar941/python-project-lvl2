#!/usr/bin/env/python3
"""module gendiff"""
import argparse
from gendiff import parce, diff, read_file
from gendiff.formatters import stylish, plain, to_json


def generate_diff(f_1, f_2, f='stylish'):
    """
    main code

    Returns:
        str
    """
    diffs = diff.get_diff(read_file.read(f_1), read_file.read(f_2))
    if f == 'plain':
        print(plain.formatter(diffs))
        return plain.formatter(diffs)
    elif f == 'json':
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

