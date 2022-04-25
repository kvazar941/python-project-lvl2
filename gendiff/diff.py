"""Diff module."""

OLD = 'old'
NEW = 'new'
KEY = 'key'
DIFF = 'diff'
CHILDREN = 'children'


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


def is_key_no_change(node):
    return get_diff_node(node).get(OLD) == get_diff_node(node).get(NEW)


def is_key_change(node):
    return not is_key_no_change(node)


def is_key_added(node):
    return OLD not in get_diff_node(node)


def is_key_removed(node):
    return NEW not in get_diff_node(node)


def is_key_updated(node):
    if OLD in get_diff_node(node) and NEW in get_diff_node(node):
        return get_diff_old(node) != get_diff_new(node)
    return False


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
        return {KEY: key, CHILDREN: get_diff(dict_a[key], dict_b[key])}
    node = {}
    if key in dict_a:
        node[OLD] = dict_a.get(key)
    if key in dict_b:
        node[NEW] = dict_b.get(key)
    return {KEY: key, DIFF: node}


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
