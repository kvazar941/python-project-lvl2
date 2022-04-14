"""Plain module."""
from gendiff.diff import (get_children, get_diff_new, get_diff_old, get_key,
                          is_key_added, is_key_removed, is_key_updated,
                          is_node, is_not_node)
from gendiff.formatters.convert_bool import convert

COMPLEX_VALUE = '[complex value]'


def format_conv(value):
    if value in [True, False, None]:
        return convert(value)
    else:
        return f"'{value}'"


def is_complex(value):
    return COMPLEX_VALUE if isinstance(value, dict) else format_conv(value)


def create_string_add_key(way, node):
    way_result = way + get_key(node)
    value = is_complex(get_diff_new(node))
    return f"Property '{way_result}' was added with value: {value}\n"

    
def create_string_removed_key(way, node):
    return f"Property '{way + get_key(node)}' was removed\n"


def create_string_updated_key(way, node):
    way_result = way + get_key(node)
    old = is_complex(get_diff_old(node))
    new = is_complex(get_diff_new(node))
    return f"Property '{way_result}' was updated. From {old} to {new}\n"


def formatter(list_, way=''):
    """
    The function converts the format 
    [
        {'key': key, 'diff': {'old': old, 'new': new}},
        {'key': key, 'children': ['children']},
        ...
    ] 
    to string format
    Property 'way.key' was added with value: new
    Property 'way.key' was removed
    Property 'way.key' was updated. From old to new
    ...
    .
    Args:
        list_: list
        count: int
        way: str

    Returns: str

    """

    list_sorted = sorted(list_, key = lambda x: get_key(x))
    result = ''
    for node in list_sorted:
        #result += create_string_node(node)
        if is_node(node):
            if is_key_added(node):
                result += create_string_add_key(way, node)
            if is_key_removed(node):
                result += create_string_removed_key(way, node)
            if is_key_updated(node):
                result += create_string_updated_key(way, node)
        else:
            result += formatter(get_children(node), way + get_key(node) + '.')
    return result

