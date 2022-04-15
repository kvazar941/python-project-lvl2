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


def convert_dict(dict_, count):
    if not isinstance(dict_, dict):
        return convert(dict_)
    indent = DEFAULT_INDENT * (count + 1)
    list_result = []
    for node in dict_:
        children = convert_dict(dict_[node], count + 1)
        list_result.append((indent, node, children))
    return list_result


def get_list_changed(node, indent, count):
    """
    The function converts the format.

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


def convert_format(list_, count_recursion=0):
    """
    The function converts the format.

        Convert format from {key: 'key', diff: {'old': old, 'new': new}}
                         to ('    ', key, old/new)

    Args:
        list_: list
        count_recursion: int

    Returns:
        list
    """
    indent = DEFAULT_INDENT * count_recursion
    indent_result = indent + DEFAULT_INDENT
    result = []

    for node in filter(is_node, list_):
        result.extend(get_list_changed(node, indent, count_recursion + 1))
    for node in filter(is_not_node, list_):
        value = convert_format(get_children(node), count_recursion + 1)
        result.append((indent_result, get_key(node), value))
    return sorted(result, key=lambda key_node: key_node[1])


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
    #if not isinstance(list_tuple, list):
    #    return '{0}{1}: {2}'.format(*list_tuple)
    
    #children = 
    def is_list(checked_value):
        if isinstance(checked_value, list):
            return f'{convert_to_str(checked_value, count + 1)}'
        return f'{checked_value}\n'
    list_string = []
    for tuple_ in list_tuple:
        indent, key, key_value = tuple_
        list_string.append(f'{indent}{key}: {is_list(key_value)}')
    return '{\n' + ''.join(list_string) + DEFAULT_INDENT * count + '}\n'


def formatter(list_):
    return convert_to_str(convert_format(list_))
