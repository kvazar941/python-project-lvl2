#!/usr/bin/env/python3
"""module gendiff."""
from gendiff.difference_logic import generate_diff
from gendiff.parsing import argument_handing


def main():
    args = argument_handing()
    generate_diff(args.first_file, args.second_file, args.format)


if __name__ == '__main__':
    main()
