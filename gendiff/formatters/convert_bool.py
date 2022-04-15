"""convert_bool module."""


def convert(checked_value):
    if checked_value is True:
        return 'true'
    elif checked_value is False:
        return 'false'
    elif checked_value is None:
        return 'null'
    return checked_value
