"""Diff module"""


def dict_list2(dict_):
    result = []
    if type(dict_) != dict:
        return dict_
    for z in dict_:
        if type(dict_[z]) == dict:
            result.append({'key': z, 'children': dict_list2(dict_[z])})
        else:
            result.append({'key': z, 'diff': {'new': dict_[z]}})
    return result


def diff_of_list(dict_a, dict_b):
    result = []
    a_set = dict_a.keys() - dict_b.keys()
    b_set = dict_b.keys() - dict_a.keys()
    ch_set = dict_a.keys() & dict_b.keys()
    
    for a in a_set:
        if type(dict_a[a]) == dict:
            result.append({'key': a, 'value': dict_list2(dict_a[a])})
        else:
            result.append({'key': a, 'diff': {'old': dict_a[a]}}) 
    for a in b_set:
        if type(dict_b[a]) == dict:
            result.append({'key': a, 'value': dict_list2(dict_b[a])})
        else:
            result.append({'key': a, 'diff': {'new': dict_b[a]}})
    for a in ch_set:
        if type(dict_a[a]) == dict and type(dict_b[a]) == dict:
            result.append({'key': a, 'children': diff_of_list(dict_a[a], dict_b[a])})
        else:
            #if type(dict_a[a]) == dict:
            #    res_a = {'key': a, 'value': dict_list2(dict_a[a])}
            #else:
            #    res_a = {'key': a, 'diff': {'old': dict_a[a]}}
            #if type(dict_b[a]) == dict:
            #    res_b = {'key': a, 'value': dict_list2(dict_b[a])}
            #else:
            #    res_b = {'key': a, 'diff': {'new': dict_b[a]}}
            

            result.append({'key': a, 'diff': {'old': dict_list2(dict_a[a]), 'new': dict_list2(dict_b[a])}})
            #result.append({'key': a, 'diff': {'old': dict_a[a], 'new': dict_b[a]}})

    #print(result)
    return result

