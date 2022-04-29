"""Stylish module."""
from gendiff.diff import (ADDED, DELETED, MODIFIED, NOT_MODIFIED, STATUS,
                          get_children, get_diff_new, get_diff_old, get_key)
from gendiff.formatters.convert_bool import convert

DEFAULT_INDENT = '    '


def formate(current_indent, key, content_key, count):
    """
    Get the complex value formatted.

    Args:
        current_indent: str
        key: str
        content_key: any
        count: int

    Returns:
        list
    """
    if not isinstance(content_key, dict):
        return '{0}{1}: {2}'.format(current_indent, key, convert(content_key))
    new_count = count + 1
    indent = DEFAULT_INDENT * (new_count)
    list_elem = []
    for elem in content_key:
        list_elem.append(formate(indent, elem, content_key[elem], new_count))
    list_elem.insert(0, '{')
    list_elem.append(''.join([DEFAULT_INDENT * count, '}']))
    return '{0}{1}: {2}'.format(current_indent, key, '\n'.join(list_elem))


def get_string(node, count):
    """
    Get a list of key changes.

    Args:
        node: dict
        count: int

    Returns:
        list
    """
    key = get_key(node)
    if node[STATUS] == NOT_MODIFIED:
        return [formate('    ', key, get_diff_new(node), count)]
    if node[STATUS] == ADDED:
        return [formate('  + ', key, get_diff_new(node), count)]
    if node[STATUS] == DELETED:
        return [formate('  - ', key, get_diff_old(node), count)]
    if node[STATUS] == MODIFIED:
        first_string = formate('  - ', key, get_diff_old(node), count)
        second_string = formate('  + ', key, get_diff_new(node), count)
        return [first_string, second_string]
    return [formate('    ', key, formatter(get_children(node), count), count)]


def formatter(list_dict, count=0):
    """
    Create a new format.

    Args:
        list_dict: list
        count: int

    Returns:
        list
    """
    new_count = count + 1
    indent = DEFAULT_INDENT * count
    list_string = []
    list_dict.sort(key=lambda node: node['key'])
    for dict_ in list_dict:
        string = [f'{indent}{str_}' for str_ in get_string(dict_, new_count)]
        list_string.append('\n'.join(string))
    list_string.insert(0, '{')
    list_string.append(''.join([indent, '}']))
    return '\n'.join(list_string)
