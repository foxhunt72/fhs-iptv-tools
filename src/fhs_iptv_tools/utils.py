"""File for multipe utils."""


def check_search_filter_in_string(full_string, search_string):
    """Check if search filter in sttring.

    Todo: make a regex posible

    Args:
        full_string: string to search in
        search_string: (sub)string to search for

    Returns:
        match: boolean
    """
    if search_string == full_string:
        return True

    if search_string in full_string:
        return True
    return False
