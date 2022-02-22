#!/usr/bin/env/python3
"""module gendiff"""
import argparse
import json


parser = argparse.ArgumentParser(description='Generate diff')
parser.add_argument('first_file')
parser.add_argument('second_file')
parser.add_argument('-f', '--format', help='set format of output')
args = parser.parse_args()



def convert_bool(value):
    if value == True:
        return 'true'
    elif value == False:
        return 'false'
    return value


def generate_diff(file1=args.first_file, file2=args.second_file):
    """
    main code

    Returns:
        str
    """    
    first_f = json.load(open(file1))
    second_f = json.load(open(file2))
    key_set = sorted({key for key in first_f} | {key for key in second_f})
    result = '{\n'
    for a in key_set:
        if a in first_f and a in second_f and first_f[a] == second_f[a]:
            result += "    {0}: {1}\n".format(a, convert_bool(second_f[a]))
        elif a in first_f and a in second_f and first_f[a] != second_f[a]:
            result += " -  {0}: {1}\n".format(a, convert_bool(first_f[a]))
            result += " +  {0}: {1}\n".format(a, convert_bool(second_f[a]))
        elif a in first_f and a not in second_f:
            result += " -  {0}: {1}\n".format(a, convert_bool(first_f[a]))
        elif a not in first_f and a in second_f:
            result += " +  {0}: {1}\n".format(a, convert_bool(second_f[a]))
    result = result + '}'
    return result


if __name__ == '__main__':
    generate_diff()
