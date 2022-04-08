"""Plain module"""
from gendiff.formatters.convert_bool import convert


def format_conv(value):
    if value in [True, False, None]:
        return convert(value)
    else:
        return f"'{value}'"


def add_key(way, value):
    return f"Property '{way}' was added with value: {value}\n"


def rem_key(way):
    return f"Property '{way}' was removed\n"


def upd_key(way, old, new):
    return f"Property '{way}' was updated. From {old} to {new}\n"


def func_add(way, key, diff):
    value = '[complex value]'
    if not isinstance(diff['new'], dict):
        value = format_conv(diff['new'])
    return f"Property '{way + key}' was added with value: {value}\n"

    
def func_rem(way, a):
    return rem_key(way + a['key'])


def func_upd(way, a):
    diff_ = a['diff']
    if type(diff_['old']) == dict and type(diff_['new']) != dict:
        return upd_key(way + a['key'], '[complex value]', format_conv(diff_['new']))
    elif type(diff_['old']) != dict and type(diff_['new']) == dict:
        return upd_key(way + a['key'], format_conv(diff_['old']), '[complex value]')
    else:
        if diff_['old'] != diff_['new']:
            return upd_key(way + a['key'], format_conv(diff_['old']), format_conv(diff_['new']))
    return ''


def formatter(list_, count=0, way=''):
    list_sorted = sorted(list_, key = lambda x: x['key'])
    result = ''
    for a in list_sorted:
        if 'diff' in a:
            diff_ = a['diff']
            if 'old' not in diff_:
                result += func_add(way, a['key'], a['diff'])
            if 'new' not in diff_:
                result += func_rem(way, a)
            if 'new' in diff_ and 'old' in diff_:
                result += func_upd(way, a)
        else:
            result += formatter(a['children'], count + 1, way + a['key'] + '.')
    return result

