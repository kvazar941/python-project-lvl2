"""Diff module"""


def convert_bool(value):
    if value == True:
        return 'true'
    elif value == False:
        return 'false'
    elif value == None:
        return 'null'
    return value


def convert_to_node(key, value, diff):
    if type(value) == dict:
        result = {'key': key,
                'type': 'dict',
                'diff': diff,
                'children': [value]
                }
    elif type(value) == list:
        result = {'key': key,
                'type': 'dict',
                'diff': diff,
                'children': value
                }
    else:
        result = {'key': key,
                'type': 'elem',
                'diff': diff,
                #'value': value
                }
    return result


def dict_list2(dict_):
    result = []
    for z in dict_:
        if type(dict_[z]) == dict:
            result.append({'key': z, 'children': dict_list2(dict_[z])})
        else:
            result.append({'key': z, 'diff': {'new': dict_[z]}})
    return result


def func4(elem, key, value_one, value_two):
    diff = {'old': value_one, 'new': value_two}
    if type(elem) == dict:
        return convert_to_node(key, convert_bool(dict_list2(elem)), diff)
    else:
        return convert_to_node(key, convert_bool(elem), diff)


def create_tree(dict_):
    result = {}
    for a in dict_:
        result[a] = {'diff': {'old': dict_[a]}}
    return result


def create_tree2(dict_):
    result = {}
    for a in dict_:
        result[a] = {'diff': {'new': dict_[a]}}
    return result


def diff_of_list(dict_a, dict_b):
    key_set = sorted(dict_a.keys() | dict_b.keys())
    result = []
    a_set = dict_a.keys() - dict_b.keys()
    b_set = dict_b.keys() - dict_a.keys()
    ch_set = dict_a.keys() & dict_b.keys()
    
    for a in a_set:
        #if type(dict_a[a]) == dict:
        #    result.append({'key': a, 'children': dict_list2(dict_a[a])})
        #else:
        result.append({'key': a, 'diff': {'old': dict_a[a]}})
    for a in b_set:
        #if type(dict_b[a]) == dict:
        #result.append({'key': a, 'children': dict_list2(dict_b[a])})
        #else:
        result.append({'key': a, 'diff': {'new': dict_b[a]}})
    for a in ch_set:
        if type(dict_a[a]) == dict and type(dict_b[a]) == dict:
            result.append({'key': a, 'children': diff_of_list(dict_a[a], dict_b[a])})
        else:
            result.append({'key': a,
                'diff': {'old': dict_a[a], 'new': dict_b[a]}
                })


        '''
        if a in dict_a and a in dict_b:
            argum = (a, convert_bool(dict_a[a]), convert_bool(dict_b[a]))
            if type(dict_a[a]) == dict and type(dict_b[a]) == dict:
                result.append(func4(diff_of_list(dict_a[a], dict_b[a]), *argum))
            else:
                #if dict_a[a] != dict_b[a]:
                #    result.append(func4(dict_a[a], *argum))
                result.append(func4(dict_a[a], *argum))
        if a in dict_a and a not in dict_b:
            result.append(func4(dict_a[a], a, convert_bool(dict_a[a]), None))
        if a not in dict_a and a in dict_b:
            result.append(func4(dict_b[a], a, None, convert_bool(dict_b[a])))
        '''
    x = create_tree(dict_a)
    y = create_tree2(dict_b)

    #print(x)
    #print(y)

    #print(result)
    return result

