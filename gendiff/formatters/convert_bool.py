"""convert_bool module."""


def convert(checked_value):
    """
    Сonvert logic.

    Args:
        checked_value: Any

    Returns:
        Any
    """
    if checked_value is True:
        return 'true'
    elif checked_value is False:
        return 'false'
    elif checked_value is None:
        return 'null'
    return checked_value
