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
                'value': value
                }
    return result


def dict_list2(list_):
    result = []
    for z in list_:
        #argum = {'old': '', 'new': ''}
        argum = {'old': convert_bool(list_[z]), 'new': convert_bool(list_[z])}
        if type(list_[z]) == dict:
            result.append(convert_to_node(z, dict_list2(list_[z]), argum))
        else:
            result.append(convert_to_node(z, convert_bool(list_[z]), argum))
    return result


def func4(elem, key, value_one, value_two):
    diff = {'old': value_one, 'new': value_two}
    if type(elem) == dict:
        return convert_to_node(key, convert_bool(dict_list2(elem)), diff)
    else:
        return convert_to_node(key, convert_bool(elem), diff)


def diff_of_list(dict_a, dict_b):
    key_set = sorted(dict_a.keys() | dict_b.keys())
    result = []
    for a in key_set:
        if a in dict_a and a in dict_b:
            argum = (a, convert_bool(dict_a[a]), convert_bool(dict_b[a]))
            if type(dict_a[a]) == dict and type(dict_b[a]) == dict:
                result.append(func4(diff_of_list(dict_a[a], dict_b[a]), *argum))
            else:
                if dict_a[a] == dict_b[a]:
                    result.append(func4(dict_b[a], *argum))
                if dict_a[a] != dict_b[a]:
                    result.append(func4(dict_a[a], *argum))
                    result.append(func4(dict_b[a], *argum))
        if a in dict_a and a not in dict_b:
            result.append(func4(dict_a[a], a, convert_bool(dict_a[a]), None))
        if a not in dict_a and a in dict_b:
            result.append(func4(dict_b[a], a, None, convert_bool(dict_b[a])))
    return result

