"""Stylish module."""
from gendiff.diff import (get_children, get_diff_new, get_diff_node, get_key,
                          is_key_no_change, is_new, is_node, is_not_node,
                          is_old)
from gendiff.formatters.convert_bool import convert

DEFAULT_INDENT = '    '


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
    if is_key_no_change(node):
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
    list_tuple = []
    indent = DEFAULT_INDENT * count
    for node in filter(is_node, list_dict):
        list_tuple.extend(get_list_changed(node, indent, count + 1))
    for key in filter(is_not_node, list_dict):
        curr_value = convert_format(get_children(key), count + 1)
        list_tuple.append((indent + DEFAULT_INDENT, get_key(key), curr_value))
    return sorted(list_tuple, key=lambda key_node: key_node[1])


def convert_to_str(list_tuple, count=0):
    """
    Create a one string from node.

    Args:
        list_tuple: list
        count: int

    Returns:
        str
    """
    list_string = []

    def is_list(checked_value):
        if isinstance(checked_value, list):
            return f'{convert_to_str(checked_value, count + 1)}'
        return f'{checked_value}\n'
    list_string = []
    for tuple_ in list_tuple:
        indent, key, key_value = tuple_
        list_string.append(f'{indent}{key}: {is_list(key_value)}')
    if count > 0:
        return '{\n' + ''.join(list_string) + DEFAULT_INDENT * count + '}\n'
    return '{\n' + ''.join(list_string) + DEFAULT_INDENT * count + '}'


def formatter(list_):
    return convert_to_str(convert_format(list_))
