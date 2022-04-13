"""to json module"""
from gendiff.formatters.convert_bool import convert
from gendiff.diff import get_key, get_diff_node, get_children
from gendiff.diff import is_node, is_not_node


DEFOLT_INDENT = '  '


def formate_value(dict_):
    return {key: convert(dict_[key]) for key in dict_}


def formatter(list_, count=0):
    list_sorted = sorted(list_, key = lambda x: get_key(x))
    result = '{\n'
    for element in list_sorted:
        if is_node(element):
            value = formate_value(get_diff_node(element))
        else:
            value = formatter(get_children(element), count + 1)
        result += f"{DEFOLT_INDENT*(count + 1)}'{get_key(element)}': {value}\n"
    result += DEFOLT_INDENT*count + '}'
    result += '\n' if count == 0 else ''
    return result
