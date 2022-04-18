"""to json module."""
import json

from gendiff.diff import get_children, get_diff_node, get_key, is_node


def get_format(list_):
    list_sorted = sorted(list_, key=lambda node: get_key(node))
    dict_result = {}
    for element in list_sorted:
        if is_node(element):
            dict_result[get_key(element)] = get_diff_node(element)
        else:
            dict_result[get_key(element)] = get_format(get_children(element))
    return dict_result


def formatter(list_):
    return json.dumps(get_format(list_), indent=4)
