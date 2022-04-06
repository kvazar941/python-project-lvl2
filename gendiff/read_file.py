#!/usr/bin/env/python3
"""module read_file"""
import json, yaml


def read(way_to_file):
    """
    Read file.

    Returns:
        dict
    """
    if way_to_file.split('.')[-1] == 'json':
        return json.load(open(way_to_file))
    if way_to_file.split('.')[-1] in ['yml', 'yaml']:
        with open(way_to_file) as file_yaml:
            return yaml.load(file_yaml, Loader=yaml.FullLoader)
