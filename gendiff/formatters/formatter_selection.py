"""module formatter_selection."""
from gendiff.formatters import json, plain, stylish

STYLISH = 'stylish'
PLAIN = 'plain'
JSON = 'json'


def apply_formatter(selected_format, diffs):
    if selected_format == STYLISH:
        string_result = stylish.formatter(diffs)
    if selected_format == PLAIN:
        string_result = plain.formatter(diffs)
    if selected_format == JSON:
        string_result = json.formatter(diffs)
    print(string_result)
    return string_result
