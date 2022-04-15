#!/usr/bin/env/python3
"""module gendiff."""
from gendiff import parce
from gendiff.engine import generate_diff


def main():
    args = parce.parce_file()
    generate_diff(args.first_file, args.second_file, args.format)


if __name__ == '__main__':
    main()
