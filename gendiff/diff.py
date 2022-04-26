"""Diff module."""

OLD = 'old'
NEW = 'new'
KEY = 'key'
DIFF = 'diff'
CHILDREN = 'children'
STATUS = 'status'
DELETED = 'deleted'
ADDED = 'added'
MODIFIED = 'modified'
NOT_MODIFIED = 'not modified'
NESTED = 'nested'


def is_all_dict(*args):
    return all([isinstance(argument, dict) for argument in args])


def is_old(key):
    return key == OLD


def is_new(key):
    return key == NEW


def get_key(node):
    return node[KEY]


def get_diff_node(node):
    return node[DIFF]


def get_diff_old(node):
    return node[DIFF][OLD]


def get_diff_new(node):
    return node[DIFF][NEW]


def get_children(node):
    return node[CHILDREN]


def is_node(node):
    return DIFF in node


def is_not_node(node):
    return CHILDREN in node


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
    def get_key_status(cheked_key):
        status = NOT_MODIFIED
        if cheked_key not in dict_a:
            status = ADDED
        elif cheked_key not in dict_b:
            status = DELETED
        elif dict_a[cheked_key] != dict_b[cheked_key]:
            status = MODIFIED
        return status

    if is_all_dict(dict_a.get(key), dict_b.get(key)):
        children = get_diff(dict_a[key], dict_b[key])
        return {KEY: key, CHILDREN: children, STATUS: NESTED}
    node = {}
    if key in dict_a:
        node[OLD] = dict_a.get(key)
    if key in dict_b:
        node[NEW] = dict_b.get(key)
    return {KEY: key, DIFF: node, STATUS: get_key_status(key)}


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
