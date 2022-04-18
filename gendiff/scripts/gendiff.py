#!/usr/bin/env/python3
"""module gendiff."""
from gendiff import diff, parce, read_file
from gendiff.formatters import json, plain, stylish


def generate_diff(first_file, second_file, output_format='stylish'):
    """
    Display the difference between files in the selected format.

    Args:
        first_file: list
        second_file: int
        output_format: str

    Returns:
        list
    """
    data_first_file = read_file.read(first_file)
    data_second_file = read_file.read(second_file)
    diffs = diff.get_diff(data_first_file, data_second_file)
    if output_format == 'plain':
        return plain.formatter(diffs)
    if output_format == 'json':
        return json.formatter(diffs)
    return stylish.formatter(diffs)


def main():
    args = parce.parce_file()
    generate_diff(args.first_file, args.second_file, args.format)


if __name__ == '__main__':
    main()
