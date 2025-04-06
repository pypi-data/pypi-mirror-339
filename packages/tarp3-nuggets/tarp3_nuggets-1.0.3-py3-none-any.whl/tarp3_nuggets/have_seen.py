"""
A function to see if a list item has been seen before
"""
def have_seen(passed_item, passed_list)->bool:
    """ Given a value and a list, check if we've seen the value before"""
    got_one = False
    for item in passed_list:
        if item == passed_item:
            got_one = True
            break
    return got_one
