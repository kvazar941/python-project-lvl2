"""Stylish module"""


def convert_bool(value):
    if value == True:
        return 'true'
    elif value == False:
        return 'false'
    elif value == None:
        return 'null'
    return value


def func_add(a, count):
    diff_ = a['diff']
    return "{0}{1}: {2}\n".format('    '*count + '  + ', a['key'], convert_bool(diff_['new']))


def func_add_dict(dict_, count):
    result = ''
    if type(dict_) == list:
        result += "{0}{1}: {2}\n".format('    '*count + '    ', dict_['key'], dict_)
    else:
        result += "{0}{1}: {2}\n".format('    '*count + '    ', dict_['key'], dict_)
    return result
        


def func_rem(a, count):
    diff_ = a['diff']
    return "{0}{1}: {2}\n".format('    '*count + '  - ', a['key'], convert_bool(diff_['old']))


def func_ch(a, count):
    diff_ = a['diff']
    return "{0}{1}: {2}\n".format('    '*count + '    ', a['key'], convert_bool(diff_['new']))


def func1(list_, count):
    list_sorted = sorted(list_, key = lambda x: x['key'])
    result = '{\n'
    for a in list_sorted:
        if 'diff' in a:
            diff_ = a['diff']
            if 'new' in diff_ and 'old' not in diff_:
                result += "{0}{1}: {2}\n".format('    '*count + '    ', a['key'], convert_bool(diff_['new']))
        elif 'children' in a:
            result += "{0}{1}: {2}\n".format('    '*count + '    ', a['key'], func1(a['children'], count + 1))

    result += '    '*count + '}'
    return result


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
        elif 'children' in a:
            result += "{0}{1}: {2}\n".format('    '*count + '    ', a['key'], formatter(a['children'], count + 1))
        else:
            result += "{0}{1}: {2}\n".format('    '*count + '  * ', a['key'], func1(a['value'], count + 1))
    result += '    '*count + '}'
    return result

