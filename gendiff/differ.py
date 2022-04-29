"""module differ."""
import os

from gendiff.diff import get_diff
from gendiff.formatters.formatter_selection import apply_formatter
from gendiff.read_file import get_content, parsing_string


def get_format(way):
    if os.path.splitext(way)[1] == '.json':
        return 'json'
    if os.path.splitext(way)[1] in {'.yml', '.yaml'}:
        return 'yaml'


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
    dict_a = parsing_string(get_content(first_file), get_format(first_file))
    dict_b = parsing_string(get_content(second_file), get_format(second_file))
    diffs = get_diff(dict_a, dict_b)
    return apply_formatter(output_format, diffs)
