"""Stylish module."""
from gendiff.diff import (get_children, get_diff_new, get_diff_node, get_key,
                          is_new, is_node, is_not_node, is_old)
from gendiff.formatters.convert_bool import convert

DEFAULT_INDENT = '    '
STATUS = 'status'
DELETED = 'deleted'
ADDED = 'added'
MODIFIED = 'modified'
NOT_MODIFIED = 'not modified'
NESTED = 'nested'


def get_indent(key):
    if is_old(key):
        return '  - '
    if is_new(key):
        return '  + '


def convert_dict(complex_value, count):
    """
    Get the complex value formatted.

    Args:
        complex_value: dict
        count: int

    Returns:
        list
    """
    if not isinstance(complex_value, dict):
        return convert(complex_value)
    indent = DEFAULT_INDENT * (count + 1)
    list_result = []
    for node in complex_value:
        children = convert_dict(complex_value[node], count + 1)
        list_result.append((indent, node, children))
    return list_result


def get_list_changed(node, indent, count):
    """
    Get a list of key changes.

    Args:
        node: dict
        indent: str
        count: int

    Returns:
        list
    """
    list_changed = []
    if node[STATUS] == NOT_MODIFIED:
        current_indent = indent + DEFAULT_INDENT
        current_value = convert_dict(get_diff_new(node), count)
        return [(current_indent, get_key(node), current_value)]
    for key in get_diff_node(node):
        current_indent = indent + get_indent(key)
        current_value = convert_dict(get_diff_node(node)[key], count)
        list_changed.append((current_indent, get_key(node), current_value))
    return list_changed


def convert_format(list_dict, count=0):
    """
    Create a new format.

        Convert format from {key: 'key', diff: {'old': old, 'new': new}}
                         to ('    ', key, old/new)

    Args:
        list_dict: list
        count: int

    Returns:
        list
    """
    indent = DEFAULT_INDENT * count
    if is_node(list_dict):
        return get_list_changed(list_dict, indent, count + 1)
    if is_not_node(list_dict):
        current_value = convert_format(get_children(list_dict), count + 1)
        return [(indent + DEFAULT_INDENT, get_key(list_dict), current_value)]
    list_lists = map(lambda elem: convert_format(elem, count), list_dict)
    list_flat = [elem for sublist in list_lists for elem in sublist]
    return sorted(list_flat, key=lambda key_node: key_node[1])


def is_tuple_node(node):
    return not isinstance(node, list)


def is_tuple_not_node(node):
    return any([isinstance(elem, list) for elem in list(node)])


def get_child_tuple(node):
    for elem in node:
        if isinstance(elem, list):
            return elem


def convert_to_str(list_tuple, count=0):
    """
    Create a string from list_tuple.

    Args:
        list_tuple: list
        count: int

    Returns:
        str
    """
    if is_tuple_node(list_tuple):
        indent, key, key_value = list_tuple
        if is_tuple_not_node(list_tuple):
            new_value = convert_to_str(get_child_tuple(list_tuple), count + 1)
            return '{0}{1}: {2}'.format(indent, key, new_value)
        return '{0}{1}: {2}'.format(*list_tuple)
    string = list(map(lambda elem: convert_to_str(elem, count), list_tuple))
    string.insert(0, '{')
    string.append(''.join([DEFAULT_INDENT * count, '}']))
    return '\n'.join(string)


def formatter(list_dict):
    return convert_to_str(convert_format(list_dict))
