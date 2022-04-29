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


def get_string(node, count):  # noqa WPS210
    """
    Get a list of key changes.

    Args:
        node: dict
        count: int

    Returns:
        list
    """
    indent = DEFAULT_INDENT * (count - 1)
    key = get_key(node)
    if node[STATUS] == MODIFIED:
        first_str = formate(f'{indent}  - ', key, get_diff_old(node), count)
        second_str = formate(f'{indent}  + ', key, get_diff_new(node), count)
        return [first_str, second_str]
    elif node[STATUS] == NOT_MODIFIED:
        current_indent = DEFAULT_INDENT
        content_key = get_diff_new(node)
    elif node[STATUS] == ADDED:
        current_indent = '  + '
        content_key = get_diff_new(node)
    elif node[STATUS] == DELETED:
        current_indent = '  - '
        content_key = get_diff_old(node)
    else:
        current_indent = DEFAULT_INDENT
        content_key = formatter(get_children(node), count)
    return [formate(f'{indent}{current_indent}', key, content_key, count)]


def formatter(list_dict, count=0):
    """
    Create a new format.

    Args:
        list_dict: list
        count: int

    Returns:
        list
    """
    list_dict.sort(key=lambda node: node['key'])
    list_ = ['\n'.join(get_string(dict_, count + 1)) for dict_ in list_dict]
    list_.insert(0, '{')
    list_.append(''.join([DEFAULT_INDENT * count, '}']))
    return '\n'.join(list_)
