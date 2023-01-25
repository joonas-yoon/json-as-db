from typing import Callable


def copy_doc(original: Callable) -> Callable:
    def wrapper(target: Callable) -> Callable:
        target.__doc__ = original.__doc__
        return target
    return wrapper
