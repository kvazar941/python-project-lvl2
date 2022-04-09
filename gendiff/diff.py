"""Diff module"""


def is_all_dict(*args):
    return all([isinstance(x, dict) for x in args])


def node(key, dict_a, dict_b):
    if is_all_dict(dict_a.get(key), dict_b.get(key)):
        return {'key': key, 'children': get_diff(dict_a[key], dict_b[key])}
    else:
        elem = {}
        if key in dict_a:
            elem['old'] = dict_a[key]
        if key in dict_b:
            elem['new'] = dict_b[key]
        return {'key': key, 'diff': elem}


def get_diff(dict_a, dict_b):
    key_set = dict_a.keys() | dict_b.keys()
    return [node(key, dict_a, dict_b) for key in key_set]

