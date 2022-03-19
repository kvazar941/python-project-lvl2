#!/usr/bin/env/python3
"""module gendiff"""
from gendiff.parsing import parce
import argparse
from gendiff.formatters import stylish, plain, to_json
from gendiff.diffs import diff
import json
import yaml


args = parce.parce_file()


def read_file(item):
    if item.split('.')[-1] == 'json':
        res_js = json.load(open(item))
        return res_js
    if item.split('.')[-1] in ['yml', 'yaml']:
        with open(item) as file_yaml:
            return yaml.load(file_yaml, Loader=yaml.FullLoader)


def generate_diff(f_1=args.first_file, f_2=args.second_file, f=args.format):
    """
    main code

    Returns:
        str
    """
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

if __name__ == '__main__':
    generate_diff()
