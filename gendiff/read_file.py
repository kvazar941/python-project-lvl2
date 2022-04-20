"""module read_file."""
import json

import yaml


def read_file(way_to_file):
    with open(way_to_file) as file_name:
        return file_name.read()


def parsing_json(string):
    return json.loads(string)


def parsing_yaml(string):
    return yaml.safe_load(string)


def get_file_extension(way_to_file):
    return way_to_file.split('.')[-1]


def is_json(way_to_file):
    return get_file_extension(way_to_file) == 'json'


def is_yaml(way_to_file):
    return get_file_extension(way_to_file) in {'yml', 'yaml'}


def read_data(way_to_file):
    """
    Read file.

    Args:
        way_to_file: str

    Returns:
        dict
    """
    if is_json(way_to_file):
        return parsing_json(read_file(way_to_file))
    if is_yaml(way_to_file):
        return parsing_yaml(read_file(way_to_file))
