"""Stylish module"""


def convert_bool(value):
    if value == True:
        return 'true'
    elif value == False:
        return 'false'
    elif value == None:
        return 'null'
    return value


def func1(a, count):
    diff_ = a['diff']
    return "{0}{1}: {2}\n".format('    '*count + '  + ', a['key'], convert_bool(diff_['new']))


def func2(a, count):
    diff_ = a['diff']
    return "{0}{1}: {2}\n".format('    '*count + '  - ', a['key'], convert_bool(diff_['old']))


def func3(a, count):
    diff_ = a['diff']
    return "{0}{1}: {2}\n".format('    '*count + '    ', a['key'], convert_bool(diff_['new']))


def formatter(list_, count=0):
    list_sorted = sorted(list_, key = lambda x: x['key'])
    print(list_sorted)
    result = '{\n'
    for a in list_sorted:
        if 'diff' in a:
            diff_ = a['diff']
            if 'new' in diff_ and 'old' not in diff_:
                if type(diff_['new']) == dict:
                    result += "{0}{1}: {2}\n".format('    '*count + '  7 ', a['key'], convert_bool(diff_['new']))
                else:
                    result += func1(a, count)
            elif 'new' not in diff_ and 'old' in diff_:
                result += func2(a, count)
            elif diff_['old'] == diff_['new']:
                result += func3(a, count)
            else:
                result += func2(a, count)
                result += func1(a, count)
        else:
            result += "{0}{1}: {2}\n".format('    '*count + '    ', a['key'], formatter(a['children'], count + 1))
        '''
        else:
            if diff_old != diff_new:
                if type(diff_['old']) == dict and type(diff_['new']) != dict:
                    diff_result = '  - '
                elif type(diff_['old']) != dict and type(diff_['new']) == dict:
                    diff_result = '  + '
                elif diff_['old'] == None:
                    diff_result = '  + '
                elif diff_['new'] == None:
                    diff_result = '  - '
            result += "{0}{1}: {2}".format('    '*count + diff_result, a['key'], formatter(a['children'], count + 1))
        '''
    result += '    '*count + '}'
    result += '\n'
    return result

