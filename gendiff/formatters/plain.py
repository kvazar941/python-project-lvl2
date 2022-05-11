"""Plain module."""
from gendiff.diff import (ADDED, CHILDREN, DELETED, KEY, MODIFIED, NEW, OLD,
                          TYPE, is_node)
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
    way_result = way + node[KEY]
    added_value = is_complex(node[NEW])
    return f"Property '{way_result}' was added with value: {added_value}"


def create_string_removed_key(way, node):
    way_result = way + node[KEY]
    return f"Property '{way_result}' was removed"


def create_string_updated_key(way, node):
    way_result = way + node[KEY]
    old = is_complex(node[OLD])
    new = is_complex(node[NEW])
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
    children = node[CHILDREN]
    return formatter(children, ''.join([way, node[KEY], '.']))


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
    list_elements.sort(key=lambda node: node[KEY])
    list_string = [get_string_node(way, node) for node in list_elements]
    return '\n'.join(filter(lambda element: element != '', list_string))
