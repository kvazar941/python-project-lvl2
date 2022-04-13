"""Stylish module"""
from gendiff.formatters.convert_bool import convert


DEFAULT_INDENT = '    '


def get_indent(key):
    if key == 'old':
        indent = '  - '
    if key == 'new':
        indent = '  + '
    return indent


def is_key_no_change(dict_):
    return dict_['diff'].get('old') == dict_['diff'].get('new')


def is_key_change(dict_):
    return not is_key_no_change(dict_)


def convert_dict(dict_, count):
    if not isinstance(dict_, dict):
        return dict_
    indent = DEFAULT_INDENT * (count + 1)
    return [(indent, key, convert_dict(dict_[key], count+1)) for key in dict_]


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
    list_diff = list(filter(lambda x: 'diff' in x, list_))

    for x in filter(is_key_no_change, list_diff):
        result.append((indent_result, x['key'], x['diff']['new']))

    for y in filter(is_key_change, list_diff):
        for key in y['diff']:
            current_indent = indent + get_indent(key)
            current_value = convert_dict(y['diff'][key], count_recursion + 1)
            result.append((current_indent, y['key'], current_value))

    for b in filter(lambda x: 'children' in x, list_):
        value = convert_format(b['children'], count_recursion + 1)
        result.append((indent_result, b['key'], value))

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

