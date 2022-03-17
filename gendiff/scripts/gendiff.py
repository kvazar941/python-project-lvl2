#!/usr/bin/env/python3
"""module gendiff"""
from gendiff.parsing import parce
import json
import yaml


args = parce.parce_file()


def convert_bool(value):
    if value == True:
        return 'true'
    elif value == False:
        return 'false'
    elif value == None:
        return 'null'
    return value


def read_file(item):
    if item.split('.')[-1] == 'json':
        res_js = json.load(open(item))
        return res_js
    if item.split('.')[-1] in ['yml', 'yaml']:
        with open(item) as file_yaml:
            return yaml.load(file_yaml, Loader=yaml.FullLoader)


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


def get_key(dict_):
    return dict_.get('key')


def get_value(dict_):
    return dict_.get('value')


def get_type(dict_):
    return dict_.get('type')


def set_diff(dict_, diff):
    dict_['diff'] = diff


def dict_list2(list_df):
    result_list = []
    for z in list_df:
        if type(list_df[z]) == dict:
            result_list.append(convert_to_node(z, dict_list2(list_df[z]), {'old': convert_bool(list_df[z]), 'new': convert_bool(list_df[z])}))
        else:
            result_list.append(convert_to_node(z, convert_bool(list_df[z]), {'old': convert_bool(list_df[z]), 'new': convert_bool(list_df[z])}))
    return result_list


def diff_of_list(dict_a, dict_b, count=0):
    key_set = sorted(dict_a.keys() | dict_b.keys())
    result_dict = []
    for a in key_set:
        if a in dict_a and a in dict_b:
            if type(dict_a[a]) == dict and type(dict_b[a]) == dict:
                result_dict.append(convert_to_node(a, diff_of_list(dict_a[a], dict_b[a], count + 1), {'old': dict_a[a], 'new': dict_b[a]})) # '    '
            else:
                if dict_a[a] == dict_b[a]:
                    result_dict.append(convert_to_node(a, convert_bool(dict_b[a]), {'old': convert_bool(dict_a[a]), 'new': convert_bool(dict_b[a])})) # '    '
                if dict_a[a] != dict_b[a]:
                    if type(dict_a[a]) == dict:
                        result_dict.append(convert_to_node(a, convert_bool(dict_list2(dict_a[a])), {'old': dict_a[a], 'new': dict_b[a]})) #'  - '
                    else:
                        result_dict.append(convert_to_node(a, convert_bool(dict_a[a]), {'old': convert_bool(dict_a[a]), 'new': convert_bool(dict_b[a])})) #'  - '
                    if type(dict_b[a]) == dict:
                        result_dict.append(convert_to_node(a, convert_bool(dict_list2(dict_b[a])), {'old': dict_a[a], 'new': dict_b[a]})) #'  + '
                    else:
                        result_dict.append(convert_to_node(a, convert_bool(dict_b[a]), {'old': convert_bool(dict_a[a]), 'new': convert_bool(dict_b[a])})) #'  + '
        if a in dict_a and a not in dict_b:
            if type(dict_a[a]) == dict:
                result_dict.append(convert_to_node(a, convert_bool(dict_list2(dict_a[a])), {'old': convert_bool(dict_a[a]), 'new': None})) # '  - '
            else:
                result_dict.append(convert_to_node(a, convert_bool(dict_a[a]), {'old': convert_bool(dict_a[a]), 'new': None})) #'  - '
        if a not in dict_a and a in dict_b:
            if type(dict_b[a]) == dict:
                result_dict.append(convert_to_node(a, convert_bool(dict_list2(dict_b[a])), {'old': None, 'new': convert_bool(dict_b[a])})) # '  + '
            else:
                result_dict.append(convert_to_node(a, convert_bool(dict_b[a]), {'old': None, 'new': convert_bool(dict_b[a])})) # '  + '
    return result_dict          
    

def stylish(list_, count=0):
    result = '{\n'
    for a in list_:
        diff_ = a['diff']
        diff_old = diff_['old']
        diff_new = diff_['new']
        diff_result = '    '

        if a.get('children') == None:
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
                if a['children'] == diff_['old']:
                    diff_result = '  - '
                elif a['children'] == diff_['new']:
                    diff_result = '  + '
                elif diff_old == None:
                    diff_result = '  + '
                elif diff_new == None:
                    diff_result = '  - '
            result += "{0}{1}: {2}".format('    '*count + diff_result, a['key'], stylish(a['children'], count + 1))

    result += '    '*count + '}'
    result += '\n'
    return result


def plain2(list_):
    a_filtr = [x for x in list_ if x['diff'] != '    ']
    a_removed = {elem['key'] for elem in a_filtr if elem['diff'] == '  - '}
    a_added = {elem['key'] for elem in a_filtr if elem['diff'] == '  + '}
    a_updated = a_added & a_removed
    a_added -= a_updated
    a_removed -= a_updated
    result = ''
    print(a_added, a_removed, a_updated)
    for a in a_filtr:
        key_add = a['key']
        if a['key'] in a_added:
            if a['type'] == 'dict':
                result += plain(a['children'])
            else:
                result += "Property '" + key_add + "' was added with value: " + a['value']+ "\n"
        if a['key'] in a_removed:
            result += "Property '" + key_add + "' was removed\n"
        if a['key'] in a_updated:
            result += "Property '" + key_add + "' was updated.\n"

    print(result)
    return result


def plain(list_, way=''):
    result = ''
    add_str = 'was added with value: '
    rem_str = 'was removed'
    upd_str = 'was updated. From '
    for a in list_:
        a_diff = a['diff']
        if a['type'] == 'dict':
            plain(a['children'], way + a['key'] + '.')
        else:
            if a_diff['old'] == None:
                result += "Property '{0}' {1}{2}\n".format(way + a['key'], add_str, a_diff['new'])
            if a_diff['new'] == None:
                result += "Property '{0}' {1}\n".format(way + a['key'], rem_str) 
            if a_diff['old'] != a_diff['new'] and a_diff['old'] != None and a_diff['new'] != None:
                result += "Property '{0}' {1}{2} to {3}\n".format(way + a['key'], upd_str, a_diff['old'], a_diff['new'])
    print(result)
    return result


def generate_diff(file1=args.first_file, file2=args.second_file):
    """
    main code

    Returns:
        str
    """
    ret = diff_of_list(read_file(file1), read_file(file2))
    print(plain(ret))
    #print(stylish(ret))
    return stylish(diff_of_list(read_file(file1), read_file(file2)))

if __name__ == '__main__':
    generate_diff()
