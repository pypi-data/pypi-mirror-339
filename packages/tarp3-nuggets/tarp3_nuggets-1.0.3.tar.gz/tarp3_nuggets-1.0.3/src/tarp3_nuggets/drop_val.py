""" drop all occurrences of val from a string """

def drop_val(my_str, val):
    """
    drop all occurrences of val from a string
    """

    while val in my_str:
        my_str.remove(val)
    return my_str
