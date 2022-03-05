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
    return value


def add_str(elem, file_):
    return "{0}: {1}\n".format(elem, convert_bool(file_[elem]))


def read_file(item):
    if item.split('.')[-1] == 'json':
        res_js = json.load(open(item))
        return res_js
    if item.split('.')[-1] in ['yml', 'yaml']:
        with open(item) as file_yaml:
            return yaml.load(file_yaml, Loader=yaml.FullLoader)


def terms(key, f_1, f_2):
    if key in f_1 and key in f_2 and f_1[key] == f_2[key]:
        return '    ' + add_str(key, f_2)
    elif key in f_1 and key in f_2 and f_1[key] != f_2[key]:
        return ' -  ' + add_str(key, f_1) + ' +  ' + add_str(key, f_2)
    elif key in f_1 and key not in f_2:
        return ' -  ' + add_str(key, f_1)
    elif key not in f_1 and key in f_2:
        return ' +  ' + add_str(key, f_2)


def generate_diff(file1=args.first_file, file2=args.second_file):
    """
    main code

    Returns:
        str
    """
    
    first_f = read_file(file1)
    second_f = read_file(file2)
    key_set = sorted(first_f.keys() | second_f.keys())
    result = '{\n'
    for a in key_set:
        result += terms(a, first_f, second_f)
    result += '}\n'
    return result


if __name__ == '__main__':
    generate_diff()
