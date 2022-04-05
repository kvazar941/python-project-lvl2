#!/usr/bin/env/python3
"""module gendiff"""
from gendiff.parsing import parce
import argparse
from gendiff.formatters import stylish, plain, to_json
from gendiff.diffs import diff
import json
import yaml


def read_file(item):
    if item.split('.')[-1] == 'json':
        res_js = json.load(open(item))
        return res_js
    if item.split('.')[-1] in ['yml', 'yaml']:
        with open(item) as file_yaml:
            return yaml.load(file_yaml, Loader=yaml.FullLoader)


def generate_diff(f_1, f_2, f='stylish'):
    """
    main code

    Returns:
        str
    """
    if type(f_1) != None and type(f_2) != None and type(f) != None:
        ret = diff.diff_of_list(read_file(f_1), read_file(f_2))
        if f == 'plain':
            print(plain.formatter(ret))
            return plain.formatter(ret)
        elif f == 'json':
            print(to_json.formatter(ret))
            return to_json.formatter(ret)
        else:
            print(stylish.formatter(ret))
            return stylish.formatter(ret)


def main():
    args = parce.parce_file()
    generate_diff(args.first_file, args.second_file, args.format)

if __name__ == '__main__':
    main()

