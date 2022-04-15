"""to json module."""
from gendiff.diff import get_children, get_diff_node, get_key, is_node
from gendiff.formatters.convert_bool import convert

DEFOLT_INDENT = '  '


def formate_value(dict_):
    return {key: convert(dict_[key]) for key in dict_}


def formatter(list_, count=0):
    list_sorted = sorted(list_, key=lambda node: get_key(node))
    result_string = '{\n'
    for element in list_sorted:
        indent = DEFOLT_INDENT * (count + 1)
        if is_node(element):
            current_value = formate_value(get_diff_node(element))
        else:
            current_value = formatter(get_children(element), count + 1)
        result_string += f"{indent}'{get_key(element)}': {current_value}\n"
    result_string += f'{DEFOLT_INDENT * count}' + '}'
    result_string += '\n' if count == 0 else ''
    return result_string