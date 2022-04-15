"""module engine."""
from gendiff import diff, read_file
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
        print(plain.formatter(diffs))
        return plain.formatter(diffs)
    if output_format == 'json':
        print(json.formatter(diffs))
        return json.formatter(diffs)
    print(stylish.formatter(diffs))
    return stylish.formatter(diffs)
