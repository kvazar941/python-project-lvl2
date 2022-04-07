"""Diff module"""


def get_diff(dict_a, dict_b):
    result = []
    a_set = dict_a.keys() - dict_b.keys()
    b_set = dict_b.keys() - dict_a.keys()
    ch_set = dict_a.keys() & dict_b.keys()    
    result += [{'key': a, 'diff': {'old': dict_a[a]}} for a in a_set]
    result += [{'key': b, 'diff': {'new': dict_b[b]}} for b in b_set]
    for ch in ch_set:
        if all([isinstance(x, dict) for x in [dict_a[ch], dict_b[ch]]]):
            result += [{'key': ch, 'children': get_diff(dict_a[ch], dict_b[ch])}]
        else:
            result += [{'key': ch, 'diff': {'old': dict_a[ch], 'new': dict_b[ch]}}]
    return result

