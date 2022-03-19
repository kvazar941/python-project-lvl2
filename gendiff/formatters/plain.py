"""Plain module"""


def added(way, a):
    way = way + a['key']
    add_str = 'was added with value: '
    a_diff = a['diff']
    if type(a_diff['new']) == dict:
        res = '[complex value]'
    elif type(a_diff['new']) == str:
        res = "'" + a_diff['new'] + "'"
    else:
        res = a_diff['new']
    return "Property '{0}' {1}{2}\n".format(way, add_str, res)


def remove(way, a):
    way = way + a['key']
    rem_str = 'was removed'
    return "Property '{0}' {1}\n".format(way, rem_str)


def upd(way, a):
    way = way + a['key']
    upd_str = 'was updated. From '
    a_diff = a['diff']
    old = a_diff['old']
    new = a_diff['new']
    if type(a_diff['old']) == dict:
        res_old = '[complex value]'
    elif type(a_diff['old']) == str:
        res_old = "'" + a_diff['old'] + "'"
    else:
        res_old = a_diff['old']
    if type(a_diff['new']) == dict:
        res_new = '[complex value]'
    elif type(a_diff['new']) == str:
        res_new = "'" + a_diff['new'] + "'"
    else:
        res_new = a_diff['new']

    return "Property '{0}' {1}{2} to {3}\n".format(way, upd_str, res_old, res_new)



def formatter(list_, way='', result=set()):
    add_str = 'was added with value: '
    rem_str = 'was removed'
    upd_str = 'was updated. From '
    for a in list_:
        a_diff = a['diff']
        if a['type'] == 'dict':
            if a_diff['old'] == None:
                result.add(added(way, a))
            if a_diff['new'] == None:
                result.add(remove(way, a))
            formatter(a['children'], way + a['key'] + '.')
        else:
            if a_diff['old'] == None:
                result.add(added(way, a))
            if a_diff['new'] == None:
                result.add(remove(way, a))
            if a_diff['old'] != a_diff['new'] and a_diff['old'] != None and a_diff['new'] != None:
                result.add(upd(way, a))

    result = sorted(result)

    #print(result)
    res = ''
    for x in result:
        if x != '':
            res += x
    #print(res)
    return res

