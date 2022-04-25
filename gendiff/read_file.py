"""module read_file."""
import json
import os

import yaml


def get_file_extension(way_to_file):
    return os.path.splitext(way_to_file)[1]


def get_file_data(way_to_file):
    with open(way_to_file) as file_name:
        file_content = file_name.read()
    extension = get_file_extension(way_to_file)
    return (file_content, extension)


def parsing_json(string):
    return json.loads(string)


def parsing_yaml(string):
    return yaml.safe_load(string)


def parsing_string(file_data):
    """
    Read file.

    Args:
        file_data: tuple

    Returns:
        dict
    """
    string, extension = file_data
    if extension == '.json':
        return parsing_json(string)
    if extension in {'.yml', '.yaml'}:
        return parsing_yaml(string)
