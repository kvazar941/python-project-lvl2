"""module read_file."""
import json

import yaml


def get_content(way_to_file):
    with open(way_to_file) as file_name:
        file_content = file_name.read()
    return file_content


def parsing_json(string):
    return json.loads(string)


def parsing_yaml(string):
    return yaml.safe_load(string)


def parsing_string(string, format_string):
    """
    Read file.

    Args:
        string: str
        format_string: str

    Returns:
        dict
    """
    if format_string == 'json':
        return parsing_json(string)
    if format_string == 'yaml':
        return parsing_yaml(string)
