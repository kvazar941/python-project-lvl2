"""Stylish module."""
from gendiff.diff import (ADDED, DELETED, MODIFIED, NESTED, NEW, NOT_MODIFIED,
                          OLD, STATUS, get_children, get_diff_new,
                          get_diff_node, get_diff_old, get_key, is_node,
                          is_not_node)
from gendiff.formatters.convert_bool import convert

DEFAULT_INDENT = '    '


def formate(value, count):
    """
    Get the complex value formatted.

    Args:
        complex_value: dict
        count: int

    Returns:
        list
    """
    indent = DEFAULT_INDENT * (count + 1)
    if not isinstance(value, dict):
        return '{0}'.format(convert(value))
    result = list(map(lambda key: '{0}{1}: {2}'.format(indent, key, formate(value[key], count + 1)), value))
    result.insert(0, '{')
    result.append(''.join([DEFAULT_INDENT * count, '}']))
    return '\n'.join(result)


def get_string(node, count):
    """
    Get a list of key changes.

    Args:
        node: dict

    Returns:
        tuple
    """
    if node[STATUS] == NOT_MODIFIED:
        value = formate(get_diff_new(node), count + 1)
        return ["{0}{1}: {2}".format(DEFAULT_INDENT, get_key(node), value)]
    if node[STATUS] == ADDED:
        value = formate(get_diff_new(node), count + 1)
        return ["{0}{1}: {2}".format('  + ', get_key(node), value)]
    if node[STATUS] == DELETED:
        value = formate(get_diff_old(node), count + 1)
        return ["{0}{1}: {2}".format('  - ', get_key(node), value)]
    if node[STATUS] == MODIFIED:
        old_value = value = formate(get_diff_old(node), count + 1)
        new_value = formate(get_diff_new(node), count + 1)
        first_string = "{0}{1}: {2}".format('  - ', get_key(node), old_value)
        second_string = "{0}{1}: {2}".format('  + ', get_key(node), new_value)
        return [first_string, second_string]


def formatter(list_dict, count=0):
    """
    Create a new format.

    Args:
        list_dict: list
        count: int

    Returns:
        list
    """
    indent = DEFAULT_INDENT * (count + 1)
    result = []
    list_dict.sort(key=lambda a: a['key'])
    for x in list_dict:
        if x[STATUS] == NESTED:
            children = get_children(x)
            value = formatter(children, count+1)
            string = "{0}{1}: {2}".format(indent, get_key(x), value)
        else:
            val = []
            for y in get_string(x, count):
                val.append("{0}{1}".format(DEFAULT_INDENT * count, y))
            string = '\n'.join(val)
        result.append(string)
    result.insert(0, '{')
    result.append(''.join([DEFAULT_INDENT * count, '}'])) 
    return '\n'.join(result)
