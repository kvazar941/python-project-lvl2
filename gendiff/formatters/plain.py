"""Plain module."""
from gendiff.diff import (ADDED, DELETED, MODIFIED, TYPE, get_children,
                          get_key, get_new, get_old, is_node)
from gendiff.formatters.convert_bool import convert

COMPLEX_VALUE = '[complex value]'


def format_conv(checked_value):
    if checked_value in {True, False, None}:
        return convert(checked_value)
    return f"'{checked_value}'"


def is_complex(checked_value):
    if isinstance(checked_value, dict):
        return COMPLEX_VALUE
    return format_conv(checked_value)


def create_string_add_key(way, node):
    way_result = way + get_key(node)
    added_value = is_complex(get_new(node))
    return f"Property '{way_result}' was added with value: {added_value}"


def create_string_removed_key(way, node):
    way_result = way + get_key(node)
    return f"Property '{way_result}' was removed"


def create_string_updated_key(way, node):
    way_result = way + get_key(node)
    old = is_complex(get_old(node))
    new = is_complex(get_new(node))
    return f"Property '{way_result}' was updated. From {old} to {new}"


def get_string_node(way, node):
    """
    Create a one string from node.

    Args:
        way: str
        node: dict

    Returns:
        str
    """
    string_node = ''
    if is_node(node):
        if node[TYPE] == ADDED:
            string_node = create_string_add_key(way, node)
        elif node[TYPE] == DELETED:
            string_node = create_string_removed_key(way, node)
        elif node[TYPE] == MODIFIED:
            string_node = create_string_updated_key(way, node)
        return string_node
    return formatter(get_children(node), '{0}{1}.'.format(way, get_key(node)))


def formatter(list_elements, way=''):
    """
    Create a string in the format plain.

    New format:
    Property 'a' was added with value: value
    Property 'b' was removed
    Property 'c' was updated. From old to new.

    Args:
        list_elements: list
        way: str

    Returns:
        str
    """
    list_sorted = sorted(list_elements, key=lambda element: get_key(element))
    list_string = [get_string_node(way, node) for node in list_sorted]
    return '\n'.join(filter(lambda element: element != '', list_string))
