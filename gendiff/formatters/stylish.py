"""Stylish module"""
from gendiff.formatters.convert_bool import convert
from gendiff.diff import is_key_no_change, is_key_change
from gendiff.diff import is_old, is_new
from gendiff.diff import is_node, is_not_node
from gendiff.diff import get_key, get_diff_node, get_children
from gendiff.diff import get_diff_old, get_diff_new


DEFAULT_INDENT = '    '


def get_indent(key):
    if is_old(key):
        return '  - '
    if is_new(key):
        return '  + '


def convert_dict(dict_, count):
    if not isinstance(dict_, dict):
        return dict_
    indent = DEFAULT_INDENT * (count + 1)
    return [(indent, key, convert_dict(dict_[key], count+1)) for key in dict_]


def get_list_changed(node, indent, count):
    result = []
    for key in get_diff_node(node):
        current_indent = indent + get_indent(key)
        current_value = convert_dict(get_diff_node(node)[key], count)
        result.append((current_indent, get_key(node), current_value))
    return result


def convert_format(list_, count_recursion=0):
    """
    The function converts the format 
    [
        {'key': key, 'diff': {'old': old, 'new': new}},
        {'key': key, 'children': ['children']},
        ...
    ] 
    to 
    [
        (indent, key, value),
        (indent, key, [
            (indent, key, value)
            (indent, key, value),
        ...
        ]
        ...
    ].

    Args:
        list_: list
        count_recursion: int

    Returns: list
        
    """
    indent = DEFAULT_INDENT * count_recursion
    indent_result = indent + DEFAULT_INDENT
    result = []
    list_node = list(filter(is_node, list_))
    for node in filter(is_key_no_change, list_node):
        result.append((indent_result, get_key(node), get_diff_new(node)))
    for node in filter(is_key_change, list_node):
        result.extend(get_list_changed(node, indent, count_recursion + 1))
    for node in filter(is_not_node, list_):
        value = convert_format(get_children(node), count_recursion + 1)
        result.append((indent_result, get_key(node), value))
    return sorted(result, key = lambda x: x[1])


def convert_to_str(list_, count=0):
    """
    The function converts the format
    [
        (indent, key, value),
        (indent, key, [
            (indent, key, value)
            (indent, key, value),
        ...
        ]
        ...
    ]
    to string format: 
    {
        key: value
      + key: value
      - key: value
        key: {
            key: value
          + key: value
          - key: value
            ...
        ...
        }
    }.

    Args:
        list_: list
        count: int
    
    Returns: str

    """
    result = []
    for tuple_ in list_:
        indent, key, value = tuple_
        if isinstance(value, list):
            result.append(f"{indent}{key}: {convert_to_str(value, count + 1)}")
        else:
            result.append(f"{indent}{key}: {convert(value)}\n")
    return '{\n' + "".join(result) + DEFAULT_INDENT * count + '}\n'


def formatter(list_):
    return convert_to_str(convert_format(list_))

