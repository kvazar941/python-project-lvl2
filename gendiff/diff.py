"""Diff module."""

OLD = 'old'
NEW = 'new'
KEY = 'key'
DIFF = 'diff'
CHILDREN = 'children'
TYPE = 'type'
DELETED = 'deleted'
ADDED = 'added'
MODIFIED = 'modified'
NOT_MODIFIED = 'not modified'
NESTED = 'nested'


def is_all_dict(*args):
    return all([isinstance(argument, dict) for argument in args])


def is_node(node):
    return node[TYPE] != NESTED


def is_not_node(node):
    return node[TYPE] == NESTED


def get_key_type(cheked_key, dict_a, dict_b):
    type_ = NOT_MODIFIED
    if cheked_key not in dict_a:
        type_ = ADDED
    elif cheked_key not in dict_b:
        type_ = DELETED
    elif dict_a[cheked_key] != dict_b[cheked_key]:
        type_ = MODIFIED
    return type_


def get_data_key_change(key, dict_a, dict_b):
    """
    Create a dictionary with data about changing one key.

    Args:
        key: string
        dict_a: dict
        dict_b: dict

    Returns:
        dict
    """
    if is_all_dict(dict_a.get(key), dict_b.get(key)):
        children = get_diff(dict_a[key], dict_b[key])
        return {KEY: key, CHILDREN: children, TYPE: NESTED}
    node = {KEY: key}
    if key in dict_a:
        node[OLD] = dict_a.get(key)
    if key in dict_b:
        node[NEW] = dict_b.get(key)
    node[TYPE] = get_key_type(key, dict_a, dict_b)
    return node


def get_diff(dict_a, dict_b):
    """
    Create a list of dictionaries with change data for all keys.

    Args:
        dict_a: dict
        dict_b: dict

    Returns:
        dict
    """
    key_set = dict_a.keys() | dict_b.keys()
    return [get_data_key_change(key, dict_a, dict_b) for key in key_set]
