"""Stylish module"""
from gendiff.formatters.convert_bool import convert


DEFOLT_INDENT = '    '


def add_str(count, key, elem):
    return f"{DEFOLT_INDENT * (count + 1)}{key}: {convert(elem)}\n"


def format_dict(dict_, count):
    if not isinstance(dict_, dict):
        return dict_
    result = '{\n'
    for a in dict_:
        result += add_str(count, a, format_dict(dict_[a], count + 1))
    result += DEFOLT_INDENT*count + '}'
    return result


def elem_to_str(x, count):
    if isinstance(x['value'], list):
        value = f"{format_elem(x['value'], count + 1)}"
    elif isinstance(x['value'], dict):
        value = f"{format_dict(x['value'], count + 1)}\n"
    else:
        value = f"{convert(x['value'])}\n"
    return f"{x['indent']}{x['key']}: {value}"


def func(indent, key, value):
    return [{'indent': indent, 'key': key, 'value': value}]


def formatter2(list_, count=0):
    list_sorted = sorted(list_, key = lambda x: x['key'])
    result = []
    for dict_ in list_sorted:
        key = dict_['key']
        indent = DEFOLT_INDENT*count
        if 'diff' in dict_:
            diff = dict_['diff']
            if diff.get('old') != diff.get('new'):
                if 'old' in diff:
                    result += func(indent + '  - ', key, diff['old'])
                if 'new' in diff:
                    result += func(indent + '  + ', key, diff['new'])
            else:
                result += func(indent + '    ', key, diff['new'])
        else:
            children = dict_['children']
            result += func(indent + '    ', key, formatter2(children, count + 1))
    return result


def format_elem(list_, count=0):
    result = '{\n'
    for x in list_:
        result += elem_to_str(x, count)
    result += '    ' * count + '}\n'
    return result


def formatter(list_):
    return format_elem(formatter2(list_))

