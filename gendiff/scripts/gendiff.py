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


def dict_list(dict_df):
    result_dict = {}
    for z in dict_df:
        if type(dict_df[z]) == dict:
            result_dict['    ' + z] = convert_bool(dict_list(dict_df[z]))
        else:
            result_dict['    ' + z] = convert_bool(dict_df[z])
    return result_dict

def diff(dict_a, dict_b):
    key_set = sorted(dict_a.keys() | dict_b.keys())
    result_dict = {}
    for a in key_set:
        if a in dict_a and a in dict_b:
            if type(dict_a[a]) == dict and type(dict_b[a]) == dict:
                result_dict['    ' + a] = diff(dict_a[a], dict_b[a])
            else:
                if dict_a[a] == dict_b[a]:
                    result_dict['    ' + a] = convert_bool(dict_b[a])
                if dict_a[a] != dict_b[a]:
                    if type(dict_a[a]) == dict:
                        result_dict['  - ' + a] = dict_list(dict_a[a])
                    else:
                        result_dict['  - ' + a] = convert_bool(dict_a[a])
                    if type(dict_b[a]) == dict:
                        result_dict['  + ' + a] = dict_list(dict_b[a])
                    else:
                        result_dict['  + ' + a] = convert_bool(dict_b[a])
        if a in dict_a and a not in dict_b:
            if type(dict_a[a]) == dict:
                result_dict['  - ' + a] = dict_list(dict_a[a])
            else:
                result_dict['  - ' + a] = convert_bool(dict_a[a])
        if a not in dict_a and a in dict_b:
            if type(dict_b[a]) == dict:
                result_dict['  + ' + a] = dict_list(dict_b[a])
            else:
                result_dict['  + ' + a] = convert_bool(dict_b[a])
    return result_dict


def stylish(dict_, count=0):
    result = '{\n'
    for x, y in dict_.items():
        if type(y) == dict:
            result += '    '*count + "{0}: {1}".format(x, stylish(y, count+1))
        else:
            result += '    '*count + "{0}: {1}\n".format(x, y)
    result += '    '*count + '}\n'
    return result


def generate_diff(file1=args.first_file, file2=args.second_file):
    """
    main code

    Returns:
        str
    """
    
    return stylish(diff(read_file(file1), read_file(file2)))


if __name__ == '__main__':
    generate_diff()
