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


def generate_diff(file1=args.first_file, file2=args.second_file):
    """
    main code

    Returns:
        str
    """
    
    first_f = read_file(file1)
    second_f = read_file(file2)
    key_set = sorted({key for key in first_f} | {key for key in second_f})
    result = '{\n'
    for a in key_set:
        if a in first_f and a in second_f:
            if first_f[a] == second_f[a]:
                result += '    ' + add_str(a, second_f)
            else:
                result += ' -  ' + add_str(a, first_f)
                result += ' +  ' + add_str(a, second_f)
        elif a in first_f and a not in second_f:
            result += ' -  ' + add_str(a, first_f)
        elif a not in first_f and a in second_f:
            result += ' +  ' + add_str(a, second_f)
    result += '}\n'
    return result


if __name__ == '__main__':
    generate_diff()
