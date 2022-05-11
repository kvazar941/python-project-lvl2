"""json module."""
import json

from gendiff.diff import CHILDREN, KEY, is_not_node


def formatter(list_data):
    list_data.sort(key=lambda node: node[KEY])
    for node in list_data:
        if is_not_node(node):
            formatter(node[CHILDREN])
    return json.dumps(list_data, indent=4)
