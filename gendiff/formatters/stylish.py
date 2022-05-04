"""Stylish module."""
from gendiff.diff import (ADDED, DELETED, MODIFIED, NOT_MODIFIED, TYPE, NESTED,
                          get_children, get_key, get_new, get_old)
from gendiff.formatters.convert_bool import convert

DEFAULT_INDENT = '    '
ADD_INDENT = '  + '
DEL_INDENT = '  - '

INDENTS = {ADDED: ADD_INDENT,
        DELETED: DEL_INDENT,
        NOT_MODIFIED: DEFAULT_INDENT,
        NESTED: DEFAULT_INDENT}

METODS = {ADDED: get_new,
        DELETED: get_old,
        NOT_MODIFIED: get_new}


def formate_string_value(node_value, indent=''):
    if not isinstance(node_value, dict):
        return '{0}'.format(convert(node_value))
    next_indent = indent + DEFAULT_INDENT
    res = ['{']
    for x in node_value:
        res.append('{0}{1}: {2}'.format(next_indent, x, formate_string_value(node_value[x], next_indent)))
    res.append(''.join([indent, '}']))
    return '\n'.join(res)


def make_string_key(node, indent):
    return '{0}{1}'.format(indent, get_key(node))


def make_string_value(node, node_type):
    return formate_string_value(METODS[node_type](node)).split('\n')


def make_full_string(node, indent, node_type):
    next_indent = indent + DEFAULT_INDENT
    key = make_string_key(node, INDENTS[node_type])
    list_string = make_string_value(node, node_type)
    list_string[1:] = map(lambda x: next_indent + x, list_string[1:])
    value = '\n'.join(list_string)
    return '{0}{1}: {2}'.format(indent, key, value)


def make_string_node(node, indent):
    if node[TYPE] == MODIFIED:
        return [make_full_string(node, indent, DELETED), make_full_string(node, indent, ADDED)]
    return [make_full_string(node, indent, node[TYPE])]



def formatter(list_dict, indent=''):
    """
    Create a new format.

    Args:
        list_dict: list
        count: int

    Returns:
        list
    """
    next_indent = indent + DEFAULT_INDENT
    list_dict.sort(key=lambda node: node['key'])
    result = []
    for node in list_dict:
        if node[TYPE] == NESTED:
            key = make_string_key(node, INDENTS[NESTED])
            value = formatter(get_children(node), next_indent)
            result.append('{0}{1}: {2}'.format(indent, key, value))
        else:
            result.extend(make_string_node(node, indent))
    result.insert(0, '{')
    result.append(''.join([indent, '}']))
    return '\n'.join(result)
