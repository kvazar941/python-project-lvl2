"""Stylish module."""
from gendiff.diff import (ADDED, CHILDREN, DELETED, KEY, MODIFIED, NESTED, NEW,
                          NOT_MODIFIED, OLD, TYPE)
from gendiff.formatters.convert_bool import convert

DEFAULT_INDENT = '    '
ADD_INDENT = '  + '
DEL_INDENT = '  - '

INDENTS = {ADDED: ADD_INDENT,
           DELETED: DEL_INDENT,
           MODIFIED: [DEL_INDENT, ADD_INDENT],
           NOT_MODIFIED: DEFAULT_INDENT,
           NESTED: DEFAULT_INDENT}

METODS = {ADDED: NEW,
          DELETED: OLD,
          NOT_MODIFIED: NEW}

TYPES = {ADDED: [ADDED],
         DELETED: [DELETED],
         MODIFIED: [DELETED, ADDED],
         NOT_MODIFIED: [NOT_MODIFIED]}


def add_indent(string):
    return ''.join([DEFAULT_INDENT, string])


def get_string(arg_one, arg_two):
    return '{0}: {1}'.format(arg_one, arg_two)


def add_braces(list_string, indent):
    list_string.append('}')
    list_result = ['{']
    list_result.extend([''.join([indent, string]) for string in list_string])
    return list_result


def make_flat(list_):
    return [element for sublist in list_ for element in sublist]


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
        child = [inner(data_key[key], add_indent(indent)) for key in data_key]
        step_one = map(get_string, data_key.keys(), child)
        step_two = list(map(add_indent, step_one))
        return '\n'.join(add_braces(step_two, indent))
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
    content_key = formate_content(node[METODS[node_type]])
    first_string = get_string(node[KEY], content_key[0])
    list_result = [''.join([INDENTS[node_type], first_string])]
    list_result.extend(list(map(add_indent, content_key[1:])))
    return list_result


def make_string_node(node, indent):
    """
    Create one or two rows for one key, depending on the type.

    Args:
        node: dict
        indent: str

    Returns:
        list
    """
    if node[TYPE] == NESTED:
        children = formatter(node[CHILDREN], add_indent(indent))
        list_str = [INDENTS[NESTED], get_string(node[KEY], children)]
        return [''.join(list_str)]
    list_str = [make_full_string(node, type_) for type_ in TYPES[node[TYPE]]]
    return make_flat(list_str)


def formatter(list_dict, indent=''):
    """
    Create a formatted string for console output.

    Args:
        list_dict: list
        indent: str

    Returns:
        str
    """
    list_dict.sort(key=lambda node: node[KEY])
    list_string = [make_string_node(node, indent) for node in list_dict]
    return '\n'.join(add_braces(make_flat(list_string), indent))
