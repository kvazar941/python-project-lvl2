"""Stylish module"""
from gendiff.formatters.convert_bool import convert


DEFOLT_INDENT = '    '


def format_dict(dict_, count):
    if not isinstance(dict_, dict):
        return dict_
    result = '{\n'
    for key in dict_:
        indent = DEFOLT_INDENT * (count + 1)
        value = format_dict(dict_[key], count + 1)
        result += elem_to_str(indent, key, value, count)
    result += DEFOLT_INDENT*count + '}'
    return result


def elem_to_str(indent, key, value, count):
    if isinstance(value, list):
        val = f"{format_elem(value, count + 1)}"
    elif isinstance(value, dict):
        val = f"{format_dict(value, count + 1)}\n"
    else:
        val = f"{convert(value)}\n"
    return f"{indent}{key}: {val}"


def new_format(indent, key, value):
    return [{'indent': indent, 'key': key, 'value': value}]


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
        key = dict_['key']
        indent = DEFOLT_INDENT*count_recursion
        if 'diff' in dict_:
            diff = dict_['diff']
            if diff.get('old') != diff.get('new'):
                if 'old' in diff:
                    result += new_format(indent + '  - ', key, diff['old'])
                if 'new' in diff:
                    result += new_format(indent + '  + ', key, diff['new'])
            else:
                result += new_format(indent + '    ', key, diff['new'])
        else:
            children = dict_['children']
            value = convert_format(children, count_recursion + 1)
            result += new_format(indent + '    ', key, value)
    return result


def format_elem(list_, count=0):
    result = '{\n'
    for x in list_:
        result += elem_to_str(x['indent'], x['key'], x['value'], count)
    result += '    ' * count + '}\n'
    return result


def formatter(list_):
    return format_elem(convert_format(list_))

