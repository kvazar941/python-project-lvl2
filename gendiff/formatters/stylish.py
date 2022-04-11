"""Stylish module"""
from gendiff.formatters.convert_bool import convert


DEFOLT_INDENT = '    '


def get_indent(key):
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


def convert_format(list_, count_recursion=0):
    """
    The function converts the format {'key': key} to {}.

    Args:
        list_: list

    Returns:
        int
    """
    result = []

    list_diff = list(filter(lambda x: 'diff' in x, list_))
    list_children = list(filter(lambda x: 'children' in x, list_))

    indent = DEFOLT_INDENT*count_recursion

    #list_diff_no = list(filter(lambda x: x.get('old') != x.get('new'), list_diff))
    #list_diff_yes = list(filter(lambda x: x.get('old') == x.get('new'), list_diff))
    #for z in list_diff_yes:
        #diff_z = z['diff']
        #print(list_diff_yes)
        #result.append(new_format(indent + DEFOLT_INDENT, z['key'], diff_z['new']))
    for a in list_diff:
        diff = a['diff']
        key = a['key']
        if diff.get('old') != diff.get('new'):
            for key1 in diff:
                val = diff[key1]
                value = convert_dict(val, indent + DEFOLT_INDENT) if type(val) == dict else val
                result.append(new_format(indent + get_indent(key1), key, value))
        else:
            result.append(new_format(indent + DEFOLT_INDENT, key, diff['new']))
    for b in list_children:
        key = b['key']
        value = convert_format(b['children'], count_recursion + 1)
        result.append(new_format(indent + DEFOLT_INDENT, key, value))

    result2 = sorted(result, key = lambda x: x['key'])
    return result2 # [{}, {}, {}]


def convert_to_str(indent, key, value, count):
    if isinstance(value, list):
        return f"{indent}{key}: {format_elem(value, count + 1)}"
    return f"{indent}{key}: {convert(value)}\n"


def format_elem(list_, count=0):
    result = [convert_to_str(dict_['indent'], dict_['key'], dict_['value'], count) for dict_ in list_]
    return '{\n' + "".join(result) + DEFOLT_INDENT * count + '}\n'


def formatter(list_):
    return format_elem(convert_format(list_))

