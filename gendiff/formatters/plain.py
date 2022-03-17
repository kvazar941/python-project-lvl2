"""Plain module"""

def formatter(list_, way=''):
    result = ''
    add_str = 'was added with value: '
    rem_str = 'was removed'
    upd_str = 'was updated. From '
    for a in list_:
        a_diff = a['diff']
        if a['type'] == 'dict':
            formatter(a['children'], way + a['key'] + '.')
        else:
            if a_diff['old'] == None:
                result += "Property '{0}' {1}{2}\n".format(way + a['key'], add_str, a_diff['new'])
            if a_diff['new'] == None:
                result += "Property '{0}' {1}\n".format(way + a['key'], rem_str)
            if a_diff['old'] != a_diff['new'] and a_diff['old'] != None and a_diff['new'] != None:
                result += "Property '{0}' {1}{2} to {3}\n".format(way + a['key'], upd_str, a_diff['old'], a_diff['new'])
    print(result)
    return result

