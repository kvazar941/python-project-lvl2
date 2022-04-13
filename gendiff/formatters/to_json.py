"""to json module"""
from gendiff.formatters.convert_bool import convert


DEFOLT_INDENT = '  '


def func1(dict_):
    return {a: convert(dict_[a]) for a in dict_}


def add_str(indent, key, value):
    return f"{indent}'{key}': {value}\n"


def formatter(list_, count=0):
    list_sorted = sorted(list_, key = lambda x: x['key'])
    result = '{\n'
    for a in list_sorted:
        if 'diff' in a:
            elem = func1(a['diff'])
        else:
            elem = formatter(a['children'], count + 1)
        result += add_str(DEFOLT_INDENT*(count + 1), a['key'], elem)
    if count == 0:
        result += DEFOLT_INDENT*count + '}\n'
    else:
        result += DEFOLT_INDENT*count + '}'
    return result
