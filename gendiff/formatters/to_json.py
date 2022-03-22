"""to json module"""


def formatter(list_, count=0):
    result = '{\n'
    for a in list_:
        diff_ = a['diff']
        diff_old = diff_['old']
        diff_new = diff_['new']
        diff_result = '  '

        if a['type'] == 'elem':
            result += "{0}'{1}': {2}\n".format('  '*count + diff_result, a['key'], a['diff'])
        else:
            if type(diff_old) == dict and type(diff_new) == dict:
                result += "{0}'{1}': {2}".format('  '*count + diff_result, a['key'], formatter(a['children'], count + 1))
            else:
                result += "{0}'{1}': {2}\n".format('  '*count + diff_result, a['key'], a['diff'])

    result += '    '*count + '}'
    result += '\n'
    return result
