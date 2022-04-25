#!/usr/bin/env/python3
"""module gendiff."""
from gendiff.cli import argument_handing
from gendiff.differ import generate_diff


def main():
    args = argument_handing()
    print(generate_diff(args.first_file, args.second_file, args.format))


if __name__ == '__main__':
    main()
