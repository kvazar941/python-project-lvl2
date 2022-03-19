"""Stylish module"""


def formatter(list_, count=0):
    result = '{\n'
    for a in list_:
        diff_ = a['diff']
        diff_old = diff_['old']
        diff_new = diff_['new']
        diff_result = '    '

        if a['type'] == 'elem':
            if diff_old != diff_new:
                if a['value'] == diff_['old']:
                    diff_result = '  - '
                elif a['value'] == diff_['new']:
                    diff_result = '  + '
                elif diff_old == None:
                    diff_result = '  + '
                elif diff_new == None:
                    diff_result = '  - '

            result += "{0}{1}: {2}\n".format('    '*count + diff_result, a['key'], a['value'])
        else:
            if diff_old != diff_new:
                if type(diff_old) == dict and type(diff_new) != dict:
                    diff_result = '  - '
                elif type(diff_old) != dict and type(diff_new) == dict:
                    diff_result = '  + '
                elif diff_old == None:
                    diff_result = '  + '
                elif diff_new == None:
                    diff_result = '  - '
            result += "{0}{1}: {2}".format('    '*count + diff_result, a['key'], formatter(a['children'], count + 1))

    result += '    '*count + '}'
    result += '\n'
    return result

