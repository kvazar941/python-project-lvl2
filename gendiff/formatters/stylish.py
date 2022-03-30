"""Stylish module"""


def convert_bool(value):
    if value == True:
        return 'true'
    elif value == False:
        return 'false'
    elif value == None:
        return 'null'
    return value


def format_dict(dict_, count):
    if type(dict_) != dict:
        return dict_
    result = '{\n'
    for a in dict_:
        result += "{0}{1}: {2}\n".format('    '*count + '    ', a, format_dict(dict_[a], count + 1))
    result += '    '*count + '}'
    return result
        

def func_add(a, count):
    diff_ = a['diff']
    if type(diff_['new']) == dict:
        return "{0}{1}: {2}\n".format('    '*count + '  + ', a['key'], convert_bool(format_dict(diff_['new'], count + 1)))
    return "{0}{1}: {2}\n".format('    '*count + '  + ', a['key'], convert_bool(diff_['new']))


def func_rem(a, count):
    diff_ = a['diff']
    if type(diff_['old']) == dict:
        return "{0}{1}: {2}\n".format('    '*count + '  - ', a['key'], convert_bool(format_dict(diff_['old'], count + 1)))
    return "{0}{1}: {2}\n".format('    '*count + '  - ', a['key'], convert_bool(diff_['old']))


def func_ch(a, count):
    diff_ = a['diff']
    if type(diff_['new']) == dict:
        return "{0}{1}: {2}\n".format('    '*count + '    ', a['key'], convert_bool(format_dict(diff_['new'], count + 1)))
    return "{0}{1}: {2}\n".format('    '*count + '    ', a['key'], convert_bool(diff_['new']))


def formatter(list_, count=0):
    list_sorted = sorted(list_, key = lambda x: x['key'])
    result = '{\n'
    for a in list_sorted:
        if 'diff' in a:
            diff_ = a['diff']
            if 'new' in diff_ and 'old' not in diff_:
                result += func_add(a, count)
            elif 'new' not in diff_ and 'old' in diff_:
                result += func_rem(a, count)
            elif diff_['old'] == diff_['new']:
                result += func_ch(a, count)
            else:
                result += func_rem(a, count)
                result += func_add(a, count)
        else:
            result += "{0}{1}: {2}".format('    '*count + '    ', a['key'], formatter(a['children'], count + 1))
    result += '    '*count + '}\n'
    return result

