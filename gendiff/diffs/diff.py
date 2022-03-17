"""Diff module"""


def get_key(dict_):
    return dict_.get('key')


def get_value(dict_):
    return dict_.get('value')


def get_type(dict_):
    return dict_.get('type')


def set_diff(dict_, diff):
    dict_['diff'] = diff


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


def dict_list2(list_df):
    result_list = []
    for z in list_df:
        if type(list_df[z]) == dict:
            result_list.append(convert_to_node(z, dict_list2(list_df[z]), {'old': convert_bool(list_df[z]), 'new': convert_bool(list_df[z])}))
        else:
            result_list.append(convert_to_node(z, convert_bool(list_df[z]), {'old': convert_bool(list_df[z]), 'new': convert_bool(list_df[z])}))
    return result_list


def func1(elem_one, elem_two, key):
    diff = {'old': elem_one, 'new': elem_two}
    if type(elem_one) == dict:
        return convert_to_node(key, convert_bool(dict_list2(elem_one)), diff)
    else:
        return convert_to_node(key, convert_bool(elem_one), diff)


def func2(elem_one, elem_two, key):
    diff = {'old': elem_one, 'new': elem_two}
    if type(elem_two) == dict:
        return convert_to_node(key, convert_bool(dict_list2(elem_two)), diff)
    else:
        return convert_to_node(key, convert_bool(elem_two), diff)


def func3(elem, key):
    diff = {'old': convert_bool(elem), 'new': None}
    if type(elem) == dict:
        return convert_to_node(key, convert_bool(dict_list2(elem)), diff)
    else:
        return convert_to_node(key, convert_bool(elem), diff)


def func4(elem, key):
    diff = {'old': None, 'new': convert_bool(elem)}
    if type(elem) == dict:
        return convert_to_node(key, convert_bool(dict_list2(elem)), diff)
    else:
        return convert_to_node(key, convert_bool(elem), diff)


def diff_of_list(dict_a, dict_b):
    key_set = sorted(dict_a.keys() | dict_b.keys())
    result_dict = []
    for a in key_set:
        if a in dict_a and a in dict_b:
            if type(dict_a[a]) == dict and type(dict_b[a]) == dict:
                result_dict.append(convert_to_node(a, diff_of_list(dict_a[a], dict_b[a]), {'old': dict_a[a], 'new': dict_b[a]}))
            else:
                if dict_a[a] == dict_b[a]:
                    result_dict.append(func2(dict_a[a], dict_b[a], a))
                if dict_a[a] != dict_b[a]:
                    result_dict.append(func1(dict_a[a], dict_b[a], a))
                    result_dict.append(func2(dict_a[a], dict_b[a], a))
        if a in dict_a and a not in dict_b:
            result_dict.append(func3(dict_a[a], a))
        if a not in dict_a and a in dict_b:
            result_dict.append(func4(dict_b[a], a))
    return result_dict

