"""Plain module"""


def convert_bool(value):
    if value == True:
        return 'true'
    elif value == False:
        return 'false'
    elif value == None:
        return 'null'
    return "'{0}'".format(value)


def formatter(list_, count=0, way=''):
    list_sorted = sorted(list_, key = lambda x: x['key'])
    result = ''
    for a in list_sorted:
        if 'diff' in a:
            diff_ = a['diff']
            if 'new' in diff_ and 'old' not in diff_:
                if type(diff_['new']) == dict:
                    result += "Property '{0}' was added with value: {1}\n".format(way + a['key'], '[complex value]')
                else:
                    result += "Property '{0}' was added with value: {1}\n".format(way + a['key'], convert_bool(diff_['new']))
            if 'new' not in diff_ and 'old' in diff_:
                if type(diff_['old']) == dict:
                    result += "Property '{0}' was removed\n".format(way + a['key'])
                else:
                    result += "Property '{0}' was removed\n".format(way + a['key'])
            if 'new' in diff_ and 'old' in diff_:
                if type(diff_['old']) == dict and type(diff_['new']) != dict:
                    result += "Property '{0}' was updated. From {1} to {2}\n".format(way + a['key'], '[complex value]', convert_bool(diff_['new']))
                elif type(diff_['old']) != dict and type(diff_['new']) == dict:
                    result += "Property '{0}' was updated. From {1} to {2}\n".format(way + a['key'], convert_bool(diff_['old']), '[complex value]')
                else:
                    if diff_['old'] != diff_['new']:
                        result += "Property '{0}' was updated. From {1} to {2}\n".format(way + a['key'], convert_bool(diff_['old']), convert_bool(diff_['new']))
        if 'children' in a:
            result += formatter(a['children'], count + 1, way + a['key'] + '.')
    return result

