"""to json module."""
import json

from gendiff.diff import (get_children, get_diff_node, get_key, is_node,
                          is_not_node)


def get_format(list_data):
    """
    Create dict for formatter.

    Args:
        list_data: list

    Returns:
        dict
    """
    if is_node(list_data):
        return (get_key(list_data), get_diff_node(list_data))
    if is_not_node(list_data):
        return (get_key(list_data), get_format(get_children(list_data)))
    list_sorted = sorted(list_data, key=lambda element: get_key(element))
    return dict(map(get_format, list_sorted))


def formatter(list_data):
    return json.dumps(get_format(list_data), indent=4)
