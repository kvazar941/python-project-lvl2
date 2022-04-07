"""Stylish module"""
from gendiff.formatters.convert_bool import convert


DEFOLT_INDENT = '    '
INDENTS = {'defolt': '    ', 'new': '  + ', 'old': '  - '}


def add_str(count, indent, key, elem):
    return "{0}{1}: {2}\n".format(DEFOLT_INDENT*count + indent, key, convert(elem))


def format_dict(dict_, count):
    if not isinstance(dict_, dict):
        return dict_
    result = '{\n'
    for a in dict_:
        result += add_str(count, DEFOLT_INDENT, a, format_dict(dict_[a], count + 1))
    result += DEFOLT_INDENT*count + '}'
    return result
        

def func_add(dict_, count, key, indent=INDENTS['defolt']):
    diff_ = dict_['diff']
    if isinstance(diff_[key], dict):
        elem = format_dict(diff_[key], count + 1)
    else:
        elem = diff_[key]
    return add_str(count, indent, dict_['key'], elem)


def formatter(list_, count=0):
    list_sorted = sorted(list_, key = lambda x: x['key'])
    result = '{\n'
    for a in list_sorted:
        if 'diff' in a:
            diff_ = a['diff']
            if 'old' not in diff_:
                result += func_add(a, count, 'new', '  + ')
            elif 'new' not in diff_:
                result += func_add(a, count, 'old', '  - ')
            elif diff_['old'] == diff_['new']:
                result += func_add(a, count, 'new')
            else:
                result += func_add(a, count, 'old', '  - ')
                result += func_add(a, count, 'new', '  + ')
        else:
            result += add_str(count, DEFOLT_INDENT, a['key'], formatter(a['children'], count + 1))
    if count == 0:
        result += DEFOLT_INDENT*count + '}\n'
    else:
        result += DEFOLT_INDENT*count + '}'
    return result

