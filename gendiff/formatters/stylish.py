"""Stylish module."""
from gendiff.diff import (ADDED, DELETED, MODIFIED, NESTED, NOT_MODIFIED, TYPE,
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


def get_string(arg_one, arg_two, arg_three):
    return '{0}{1}: {2}'.format(arg_one, arg_two, arg_three)


def connect_string(*args):
    return ''.join(args)


def add_indent(string):
    return connect_string(DEFAULT_INDENT + string)


def make_key_value(content_key):
    """
    Get the contents of the key and return it as a list of strings.

    Args:
        content_key: Any

    Returns:
        list
    """
    def inner(data_key, indent):
        if not isinstance(data_key, dict):
            return str(convert(data_key))
        list_str = ['{']
        for key in data_key:
            current_value = inner(data_key[key], add_indent(indent))
            string = get_string(add_indent(indent), key, current_value)
            list_str.append(string)
        list_str.append(connect_string(indent, '}'))
        return '\n'.join(list_str)
    return inner(content_key, '').split('\n')


def make_one_string_key(node, indent, node_type):
    """
    Create a string from string for key and string for value.

    Args:
        node: dict
        indent: str
        node_type: str

    Returns:
        str
    """
    key = connect_string(INDENTS[node_type], get_key(node))
    list_string = make_key_value(METODS[node_type](node))
    
    list_result = []
    for string in list_string:
        if list_string.index(string) > 0:
            list_result.append(add_indent(indent) + string)
        else:
            list_result.append(string)
    return get_string(indent, key, '\n'.join(list_result))


def make_string_node(node, indent):
    """
    Create one or two rows for one key, depending on the type.

    Args:
        node: dict
        indent: str

    Returns:
        str
    """
    if node[TYPE] != MODIFIED:
        return [make_one_string_key(node, indent, node[TYPE])]
    string_old = make_one_string_key(node, indent, DELETED)
    string_new = make_one_string_key(node, indent, ADDED)
    return [string_old, string_new]


def formatter(list_dict, indent=''):
    """
    Create a formatted string for console output.

    Args:
        list_dict: list
        indent: str

    Returns:
        str
    """
    list_dict.sort(key=lambda node: node['key'])
    result_list = ['{']
    for node in list_dict:
        if node[TYPE] == NESTED:
            key = connect_string(INDENTS[NESTED], get_key(node))
            key_value = formatter(get_children(node), add_indent(indent))
            result_list.append(get_string(indent, key, key_value))
        else:
            result_list.extend(make_string_node(node, indent))
    result_list.append(connect_string(indent, '}'))
    return '\n'.join(result_list)
