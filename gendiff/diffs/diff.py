"""Diff module"""


def diff_of_list(dict_a, dict_b):
    result = []
    a_set = dict_a.keys() - dict_b.keys()
    b_set = dict_b.keys() - dict_a.keys()
    ch_set = dict_a.keys() & dict_b.keys()
    
    for a in a_set:
        result.append({'key': a, 'diff': {'old': dict_a[a]}}) 
    for a in b_set:
        result.append({'key': a, 'diff': {'new': dict_b[a]}})
    for a in ch_set:
        if type(dict_a[a]) == dict and type(dict_b[a]) == dict:
            result.append({'key': a, 'children': diff_of_list(dict_a[a], dict_b[a])})
        else: 
            result.append({'key': a, 'diff': {'old': dict_a[a], 'new': dict_b[a]}})
    return result

