"""module read_file."""
import json

import yaml


def read(way_to_file):
    """
    Read file.

    Args:
        way_to_file: str

    Returns:
        dict
    """
    with open(way_to_file) as file_name:
        format_file = way_to_file.split('.')[-1]
        if format_file == 'json':
            return json.load(open(way_to_file))
        if format_file in ['yml', 'yaml']:
            return yaml.load(file_name, Loader=yaml.FullLoader)
