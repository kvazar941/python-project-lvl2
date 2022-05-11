"""Stylish module."""
from gendiff.diff import (ADDED, DELETED, KEY, MODIFIED, NESTED, NOT_MODIFIED,
                          TYPE, get_children, get_new, get_old)
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
    return connect_string(DEFAULT_INDENT, string)


def get_string2(arg_one, arg_two):
    return '{0}: {1}'.format(arg_one, arg_two)


def formate_content(content_key):
    """
    Format the key value.

    Args:
        content_key: Any

    Returns:
        list
    """
    def inner(data_key, indent):
        if not isinstance(data_key, dict):
            return str(convert(data_key))
        list_string = ['{']
        child = [inner(data_key[key], add_indent(indent)) for key in data_key]
        step_one = map(get_string2, data_key.keys(), child)
        step_two = list(map(add_indent, step_one))
        step_two.append('}')
        step_three = [connect_string(indent, string) for string in step_two]
        list_string.extend(step_three)
        return '\n'.join(list_string)
    return inner(content_key, '').split('\n')


def make_full_string(node, node_type):
    """
    Create a string from string for key and string for value.

    Args:
        node: dict
        node_type: str

    Returns:
        list
    """
    list_string = formate_content(METODS[node_type](node))
    list_string[0] = get_string2(node[KEY], list_string[0])
    list_result = []
    for string in list_string:
        if list_string.index(string) == 0:
            string_result = INDENTS[node_type] + string
        else:
            string_result = add_indent(string)
        list_result.append(string_result)
    return list_result


def make_string_node(node):
    """
    Create one or two rows for one key, depending on the type.

    Args:
        node: dict

    Returns:
        list
    """
    if node[TYPE] != MODIFIED:
        return make_full_string(node, node[TYPE])
    list_string = []
    list_string.extend(make_full_string(node, DELETED))
    list_string.extend(make_full_string(node, ADDED))
    return list_string


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
            child = formatter(get_children(node), add_indent(indent))
            result_list.append(get_string(INDENTS[NESTED], node[KEY], child))
        else:
            result_list.extend(make_string_node(node))
    result_list.append('}')
    res = []
    for elem in result_list:
        if result_list.index(elem) == 0:
            res.append(elem)
        else:
            res.append(indent + elem)
    return '\n'.join(res)
