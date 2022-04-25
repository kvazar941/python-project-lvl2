"""module formatter_selection."""
from gendiff.formatters import json, plain, stylish

STYLISH = 'stylish'
PLAIN = 'plain'
JSON = 'json'


def apply_formatter(selected_format, diffs):
    if selected_format == STYLISH:
        return stylish.formatter(diffs)
    if selected_format == PLAIN:
        return plain.formatter(diffs)
    if selected_format == JSON:
        return json.formatter(diffs)
