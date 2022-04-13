"""Diff module"""


def is_all_dict(*args):
    return all([isinstance(x, dict) for x in args])


def is_old(key):
    return key == 'old'


def is_new(key):
    return key == 'new'


def get_key(node):
    return node['key']


def get_diff_node(node):
    return node['diff']


def get_diff_old(node):
    return node['diff']['old']


def get_diff_new(node):
    return node['diff']['new']


def get_children(node):
    return node['children']


def is_node(node):
    return 'diff' in node


def is_not_node(node):
    return 'children' in node


def is_key_no_change(node):
    return get_diff_node(node).get('old') == get_diff_node(node).get('new')


def is_key_change(node):
    return not is_key_no_change(node)


def is_key_added(node):
    return 'old' not in get_diff_node(node)


def is_key_removed(node):
    return 'new' not in get_diff_node(node)


def is_key_updated(node):
    if 'old' in get_diff_node(node) and 'new' in get_diff_node(node):
        return get_diff_old(node) != get_diff_new(node)
    return False


def create_format(key, dict_a, dict_b):
    """
    Code.

    Args:
        num_one: int
        num_two: int

    Returns:
        int
    """
    if is_all_dict(dict_a.get(key), dict_b.get(key)):
        return {'key': key, 'children': get_diff(dict_a[key], dict_b[key])}
    node = {}
    if key in dict_a:
        node['old'] = dict_a[key]
    if key in dict_b:
        node['new'] = dict_b[key]
    return {'key': key, 'diff': node}


def get_diff(dict_a, dict_b):
    """
    Code.

    Args:
        num_one: int
        num_two: int

    Returns:
        int
    """
    key_set = dict_a.keys() | dict_b.keys()
    return [create_format(key, dict_a, dict_b) for key in key_set]

