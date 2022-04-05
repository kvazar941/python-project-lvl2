#!/usr/bin/env/python3
"""module gendiff"""
from gendiff.parsing import parce
import argparse
from gendiff.formatters import stylish, plain, to_json
from gendiff.diffs import diff
import json
import yaml

#a = parser.parse_args()
#args = parser.parse_args("first_file second_file".split())
parser = parce.parce_file()
args = parser.parse_args()
#args = parser.parse_args("first_file second_file".split())


def read_file(item):
    if item.split('.')[-1] == 'json':
        res_js = json.load(open(item))
        return res_js
    if item.split('.')[-1] in ['yml', 'yaml']:
        with open(item) as file_yaml:
            return yaml.load(file_yaml, Loader=yaml.FullLoader)


def generate_diff(f_1=args.first_file, f_2=args.second_file, f=args.format):
#def generate_diff(*args):
    #def generate_diff(*args_):
    #args = parser.parse_args("first_file second_file".split())
    print(args)
    print('module!')
    """
    main code

    Returns:
        str
    """
    print('args=', args)
    if type(f_1) != None and type(f_2) != None and type(f) != None:
        ret = diff.diff_of_list(read_file(f_1), read_file(f_2))
        print('ret = ', ret)
        if f == 'plain':
            return plain.formatter(ret)
        elif f == 'json':
            return to_json.formatter(ret)
        else:
            return stylish.formatter(ret)


def main():
    print('run at scripts!')

if __name__ == '__main__':
    print('run at scripts is --main--!')
    #main()
    generate_diff()

