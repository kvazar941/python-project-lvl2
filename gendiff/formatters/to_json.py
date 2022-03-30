"""to json module"""


def convert_bool(value):
    if value == True:
        return 'true'
    elif value == False:
        return 'false'
    elif value == None:
        return 'null'
    return value


def func1(dict_):
    dict_result = {}
    for a in dict_:
        dict_result[a] = convert_bool(dict_[a])
    return dict_result





def formatter(list_, count=0):
    list_sorted = sorted(list_, key = lambda x: x['key'])
    result = '{\n'
    for a in list_sorted:
        if 'diff' in a:
            result += "{0}'{1}': {2}\n".format('  '*count + '  ', a['key'], func1(a['diff']))
        if 'children' in a:
            result += "{0}'{1}': {2}".format('  '*count + '  ', a['key'], formatter(a['children'], count + 1))
    result += '  '*count + '}\n'
    return result
