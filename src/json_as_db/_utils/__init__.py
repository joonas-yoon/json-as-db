import copy

from typing import Any, Union, List, Tuple


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


def from_maybe_list(value: Union[Any, List[Any]]) -> Tuple[type, List[Any]]:
    return_type = type(value)
    if not isinstance(value, list):
        value = [value]
    return (return_type, value)


def return_maybe(_type: type, _values: List[Any]) -> Union[Any, List[Any]]:
    if _type is list:
        return _values
    else:
        return _values[0]
