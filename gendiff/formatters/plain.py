"""Plain module"""
from gendiff.formatters.convert_bool import convert


COMPLEX_VALUE = '[complex value]'


def format_conv(value):
    if value in [True, False, None]:
        return convert(value)
    else:
        return f"'{value}'"


def is_key_added(dict_):
    return 'old' not in dict_['diff']


def is_key_removed(dict_):
    return 'new' not in dict_['diff']


def is_key_upd(dict_):
    if 'old' in dict_['diff'] and 'new' in dict_['diff']:
        return dict_['diff']['old'] != dict_['diff']['new']
    return False


def is_complex(value):
    return COMPLEX_VALUE if isinstance(value, dict) else format_conv(value)


def add_key(way, value):
    return f"Property '{way}' was added with value: {value}\n"


def rem_key(way):
    return f"Property '{way}' was removed\n"


def upd_key(way, old, new):
    return f"Property '{way}' was updated. From {old} to {new}\n"


def func_add(way, key, diff):
    return add_key(way + key, is_complex(diff['new']))

    
def func_rem(way, key):
    return rem_key(way + key)


def func_upd(way, a):
    way_result = way + a['key']
    old = is_complex(a['diff']['old'])
    new = is_complex(a['diff']['new'])
    return upd_key(way_result, old, new)


def formatter(list_, count=0, way=''):
    """
    The function converts the format 
    [
        {'key': key, 'diff': {'old': old, 'new': new}},
        {'key': key, 'children': ['children']},
        ...
    ] 
    to string format
    Property 'way.key' was added with value: new
    Property 'way.key' was removed
    Property 'way.key' was updated. From old to new
    ...
    .
    Args:
        list_: list
        count: int
        way: str

    Returns: str

    """
    list_sorted = sorted(list_, key = lambda x: x['key'])
    result = ''

    for key in list_sorted:
        if 'diff' in key:
            if is_key_added(key):
                result += func_add(way, key['key'], key['diff'])
            if is_key_removed(key):
                result += func_rem(way, key['key'])
            if is_key_upd(key):
                result += func_upd(way, key)
        else:
            result += formatter(key['children'], count + 1, way + key['key'] + '.')
    return result

