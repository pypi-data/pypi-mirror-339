def flatten_list(nested_list: list) -> list:
    """Converts nested lists to flat ones.
    
    Example:
    >>> flatten_list([[1, 2], [3, [4]]])
    [1, 2, 3, 4]
    """
    flat_list = []
    for item in nested_list:
        if isinstance(item, list):
            flat_list.extend(flatten_list(item))
        else:
            flat_list.append(item)
    return flat_list