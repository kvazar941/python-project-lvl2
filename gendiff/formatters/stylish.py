"""Stylish module."""
from gendiff.diff import (ADDED, DELETED, KEY, MODIFIED, NESTED, NOT_MODIFIED,
                          TYPE, get_children, get_key, get_new, get_old)
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
          NOT_MODIFIED: get_new,
          MODIFIED: (get_old, get_new)}


def get_string(arg_one, arg_two, arg_three):
    return '{0}{1}: {2}'.format(arg_one, arg_two, arg_three)


def connect_string(*args):
    return ''.join(args)


def add_indent(string):
    return connect_string(DEFAULT_INDENT + string)


def add_key(key, list_string):
    list_string[0] = '{0}: {1}'.format(key, list_string[0])
    return list_string


def add_ind(type_, list_string):
    list_result = [connect_string(INDENTS[type_], list_string[0])]
    list_result.extend(list(map(add_indent, list_string[1:])))
    return list_result


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


def make_string_node(node):
    """
    Create one or two rows for one key, depending on the type.

    Args:
        node: dict

    Returns:
        list
    """
    if node[TYPE] != MODIFIED:
        b = make_key_value(METODS[node[TYPE]](node))
        return add_ind(node[TYPE], add_key(node[KEY], b))
    b1 = make_key_value(get_old(node))
    b2 = make_key_value(get_new(node))
    d1 = add_ind(DELETED, add_key(node[KEY], b1))
    d2 = add_ind(ADDED, add_key(node[KEY], b2))
    res = d1
    res.extend(d2)
    return res


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
        if node[TYPE] != NESTED:
            a = make_string_node(node)
            result_list.extend([indent + string for string in a])
        else:
            key = connect_string(INDENTS[NESTED], get_key(node))
            key_value = formatter(get_children(node), add_indent(indent))
            result_list.append(get_string(indent, key, key_value))
    result_list.append(connect_string(indent, '}'))
    return '\n'.join(result_list)
