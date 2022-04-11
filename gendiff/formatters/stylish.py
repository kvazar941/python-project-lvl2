"""Stylish module"""
from gendiff.formatters.convert_bool import convert
from functools import reduce


DEFOLT_INDENT = '    '


def get_indent(key):
    """
    The function .

    Args:
        key: str

    Returns:
        str
    """
    if key == 'old':
        indent = '  - '
    if key == 'new':
        indent = '  + '
    return indent


def new_format(indent, key, value):
    return {'indent': indent, 'key': key, 'value': value}


def convert_dict(dict_, initial_indent):
    if not isinstance(dict_, dict):
        return dict_
    indent = initial_indent + DEFOLT_INDENT
    return [new_format(indent, key, convert_dict(dict_[key], indent)) for key in dict_]


def get_diff_key(diff, key, indent):
    indent_result = indent + DEFOLT_INDENT
    result = []
    for key1 in diff:
        val = diff[key1]
        value = convert_dict(val, indent_result) if type(val) == dict else val
        result.append(new_format(indent + get_indent(key1), key, value))
    return result


def get_diff_dict(dict_, count):
    result = []
    indent = DEFOLT_INDENT*count
    key = dict_['key']
    if 'diff' in dict_:
        diff = dict_['diff']
        if diff.get('old') != diff.get('new'):
            #x = 
            result.extend(get_diff_key(diff, key, indent))
        else:
            result.append(new_format(indent + DEFOLT_INDENT, key, diff['new']))
    else:
        value = convert_format(dict_['children'], count + 1)
        result.append(new_format(indent + DEFOLT_INDENT, key, value))
    return result


def get_diff_dict2(dict_, count):
    result = []
    indent = DEFOLT_INDENT*count
    key = dict_['key']
    if 'diff' in dict_:
        diff = dict_['diff']
        if diff.get('old') != diff.get('new'):
            result.extend(get_diff_key(diff, key, indent))
        else:
            result.append(new_format(indent + DEFOLT_INDENT, key, diff['new']))
    else:
        value = convert_format(dict_['children'], count + 1)
        result.append(new_format(indent + DEFOLT_INDENT, key, value))
    return result


def convert_format(list_, count_recursion=0):
    """
    The function converts the format {'key': key} to {}.

    Args:
        list_: list

    Returns:
        int
    """
    list_sorted = sorted(list_, key = lambda x: x['key'])
    result = []
    for dict_ in list_sorted:
        result.extend(get_diff_dict(dict_, count_recursion))

    result2 = []

    list_diff = list(filter(lambda x: 'diff' in x, list_))
    indent = DEFOLT_INDENT*count_recursion
    for a in list_diff:
        diff = a['diff']
        key = a['key']
        if diff.get('old') != diff.get('new'): 
            result2.extend(get_diff_key(diff, key, indent))
        else:
            result2.append(new_format(indent + DEFOLT_INDENT, key, diff['new']))

    
    list_children = list(filter(lambda x: 'children' in x, list_))

    for b in list_children:
        key = b['key']
        value = convert_format(b['children'], count_recursion + 1)
        result2.append(new_format(indent + DEFOLT_INDENT, key, value))
    result3 = sorted(result2, key = lambda x: x['key'])
    return result3 # [{}, {}, {}]


def convert_to_str(indent, key, value, count):
    if isinstance(value, list):
        return f"{indent}{key}: {format_elem(value, count + 1)}"
    return f"{indent}{key}: {convert(value)}\n"


def format_elem(list_, count=0):
    result = [convert_to_str(dict_['indent'], dict_['key'], dict_['value'], count) for dict_ in list_]
    return '{\n' + "".join(result) + DEFOLT_INDENT * count + '}\n'


def formatter(list_):
    return format_elem(convert_format(list_))

