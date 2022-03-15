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
            result_list.append(convert_to_node(z, dict_list2(list_df[z]), '    '))
        else:
            result_list.append(convert_to_node(z, convert_bool(list_df[z]), '    '))
    return result_list


def diff_of_list(dict_a, dict_b, count=0):
    key_set = sorted(dict_a.keys() | dict_b.keys())
    result_dict = []
    for a in key_set:
        if a in dict_a and a in dict_b:
            if type(dict_a[a]) == dict and type(dict_b[a]) == dict:
                result_dict.append(convert_to_node(a, diff_of_list(dict_a[a], dict_b[a], count + 1), '    '))
            else:
                if dict_a[a] == dict_b[a]:
                    result_dict.append(convert_to_node(a, convert_bool(dict_b[a]), '    '))
                if dict_a[a] != dict_b[a]:
                    if type(dict_a[a]) == dict:
                        result_dict.append(convert_to_node(a, convert_bool(dict_list2(dict_a[a])), '  - '))
                    else:
                        result_dict.append(convert_to_node(a, convert_bool(dict_a[a]), '  - '))
                    if type(dict_b[a]) == dict:
                        result_dict.append(convert_to_node(a, convert_bool(dict_list2(dict_b[a])), '  + '))
                    else:
                        result_dict.append(convert_to_node(a, convert_bool(dict_b[a]), '  + '))
        if a in dict_a and a not in dict_b:
            if type(dict_a[a]) == dict:
                result_dict.append(convert_to_node(a, convert_bool(dict_list2(dict_a[a])), '  - '))
            else:
                result_dict.append(convert_to_node(a, convert_bool(dict_a[a]), '  - '))
        if a not in dict_a and a in dict_b:
            if type(dict_b[a]) == dict:
                result_dict.append(convert_to_node(a, convert_bool(dict_list2(dict_b[a])), '  + '))
            else:
                result_dict.append(convert_to_node(a, convert_bool(dict_b[a]), '  + '))
    return result_dict          
    

def stylish(list_, count=0):
    result = '{\n'
    for a in list_:
        if a.get('children') == None:
            result += "{0}{1}: {2}\n".format('    '*count + a['diff'], a['key'], a['value'])
        else:
            result += "{0}{1}: {2}".format('    '*count + a['diff'], a['key'], stylish(a['children'], count + 1))
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


def plain(list_):
    result = ''
    add_str = 'added with value: '
    for a in list_:
        print(len([x['key'] for x in list_ if x['key'] == a['key']]))
        add_str = 'added with value: '
        rem_str = 'removed'
        upd_str = 'updated'
        if a['diff'] == '  - ':
            result += "Property '{0}' was {1}\n".format(a['key'], rem_str)
        if a['diff'] == '  + ':
            if a['type'] == 'dict':
                result += "Property '{0}' was {1} {2}\n".format(a['key'], add_str, a['children'])
            else:
                result += "Property '{0}' was {1} {2}\n".format(a['key'], add_str, a['value'])
            


    print(result)
    return result



def generate_diff(file1=args.first_file, file2=args.second_file):
    """
    main code

    Returns:
        str
    """
    ret = diff_of_list(read_file(file1), read_file(file2))
    plain(ret)
    return stylish(diff_of_list(read_file(file1), read_file(file2)))

if __name__ == '__main__':
    generate_diff()
