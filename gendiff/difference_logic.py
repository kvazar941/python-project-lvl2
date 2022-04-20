"""module difference logic."""
from gendiff.diff import get_diff
from gendiff.formatters.formatter_selection import apply_formatter
from gendiff.read_file import read_data


def generate_diff(first_file, second_file, output_format='stylish'):
    """
    Display the difference between files in the selected format.

    Args:
        first_file: list
        second_file: int
        output_format: str

    Returns:
        str
    """
    data_first_file = read_data(first_file)
    data_second_file = read_data(second_file)
    diffs = get_diff(data_first_file, data_second_file)
    return apply_formatter(output_format, diffs)
