"""Stylish module"""
from gendiff.formatters.convert_bool import convert


DEFAULT_INDENT = '    '


def get_indent(key):
    if key == 'old':
        indent = '  - '
    if key == 'new':
        indent = '  + '
    return indent


def is_no_change(dict_):
    return dict_['diff'].get('old') == dict_['diff'].get('new')


def new_format(indent, key, value):
    return {'indent': indent, 'key': key, 'value': value}


def convert_format(list_, count_recursion=0):
    """
    The function converts the format {'key': key} to {}.

    Args:
        list_: list

    Returns:
        int
    """
    indent = DEFAULT_INDENT * count_recursion
    indent_result = indent + DEFAULT_INDENT
    result = []


    def convert_dict(dict_, count=count_recursion + 1):
        if not isinstance(dict_, dict):
            return dict_
        indent1 = DEFAULT_INDENT * (count + 1)
        return [new_format(indent1, key, convert_dict(dict_[key], count+1)) 
                for key in dict_]


    list_diff = list(filter(lambda x: 'diff' in x, list_))

    for x in filter(lambda x: is_no_change(x), list_diff):
        result.append(new_format(indent_result, x['key'], x['diff']['new']))

    for y in filter(lambda x: not is_no_change(x), list_diff):
        for key in y['diff']:
            val = y['diff'][key]
            value = convert_dict(val) if isinstance(val, dict) else val
            result.append(new_format(indent + get_indent(key), y['key'], value))
    for b in filter(lambda x: 'children' in x, list_):
        value = convert_format(b['children'], count_recursion + 1)
        result.append(new_format(indent_result, b['key'], value))

    return sorted(result, key = lambda x: x['key'])


def convert_to_str(list_, count=0):
    result = []
    for dict_ in list_:
        indent = dict_['indent']
        key = dict_['key']
        value = dict_['value']
        if isinstance(value, list):
            result.append(f"{indent}{key}: {convert_to_str(value, count + 1)}")
        else:
            result.append(f"{indent}{key}: {convert(value)}\n")
    return '{\n' + "".join(result) + DEFAULT_INDENT * count + '}\n'


def formatter(list_):
    return convert_to_str(convert_format(list_))

