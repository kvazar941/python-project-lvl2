#!/usr/bin/env/python3
"""module parce"""
import argparse


def parce_file():
    parser = argparse.ArgumentParser(description='Generate diff')
    parser.add_argument('-f', '--format', default='stylish', help='set format of output')
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    return parser.parse_args()
