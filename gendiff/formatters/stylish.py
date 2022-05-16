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


def retreat(current_indent, list_):
    list_result = [current_indent + list_[0]]
    list_result.extend(list(map(add_indent, list_[1:])))
    return list_result


def get_string(arg_one, arg_two):
    return '{0}: {1}'.format(arg_one, arg_two)


def add_braces(list_string, indent):
    list_string.append('}')
    list_result = ['{']
    list_result.extend([''.join([indent, string]) for string in list_string])
    return list_result


def make_flat(list_):
    return [element for sublist in list_ for element in sublist]


def formate(key, key_value):
    """
    Format the key value.

    Args:
        key: str
        key_value: Any

    Returns:
        list
    """
    def inner(str_one, str_two, indent=''):
        if not isinstance(str_two, dict):
            return get_string(f'{indent}{str_one}', convert(str_two))
        new_indent = add_indent(indent)
        children = [inner(key, str_two[key], new_indent) for key in str_two]
        list_result = [get_string(f'{indent}{str_one}', '{')]
        list_result.extend(children)
        list_result.append(''.join([indent, '}']))
        return '\n'.join(list_result)
    return inner(key, key_value).split('\n')


def make_full_string(node, node_type):
    """
    Create a string from string for key and string for value.

    Args:
        node: dict
        node_type: str

    Returns:
        list
    """
    full_string = formate(node[KEY], node[METODS[node_type]])
    return retreat(INDENTS[node_type], full_string)


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


def formatter(list_node, indent=''):
    """
    Create a formatted string for console output.

    Args:
        list_node: list
        indent: str

    Returns:
        str
    """
    list_node.sort(key=lambda node: node[KEY])
    list_string = [make_string_node(node, indent) for node in list_node]
    return '\n'.join(add_braces(make_flat(list_string), indent))
