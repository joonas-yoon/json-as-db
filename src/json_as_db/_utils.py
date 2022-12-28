import copy


def override_dict(__dict: dict, __target: dict) -> dict:
    """override base object if value is unset

    Args:
        __dict (dict): base object
        __target (dict): target object to override

    Returns:
        dict: overridden dictionary
    """
    unset_fields = set(__target.keys()) - set(__dict.keys())
    new_target = dict()
    for field in unset_fields:
        new_target[field] = __target[field]
    new_dict = copy.deepcopy(__dict)
    new_dict.update(new_target)
    return new_dict
