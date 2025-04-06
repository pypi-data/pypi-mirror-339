"""
print out all levels of a dictionary
"""

def get_all_levels(nested_dict, level=0):
    """
    print out all levels of a dictionary

    :param nested_dict:
    :param level:
    :return:
    """
    for key, value in nested_dict.items():
        print(f"Level {level}: {key} and type of value is {type(value)}")
        if isinstance(value, dict):
            get_all_levels(value, level + 1)
