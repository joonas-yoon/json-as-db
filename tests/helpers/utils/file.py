import os
import shutil
import inspect

from .string import random_string


def is_dir(path: str) -> bool:
    return os.path.exists(path) and os.path.isdir(path)


def mkdirs(path: str, **kwargs) -> None:
    os.makedirs(path, **kwargs)


def touch(path: str):
    with open(path, 'a'):
        os.utime(path, None)


def remove(path: str):
    if not path:
        return None
    if is_dir(path):
        shutil.rmtree(path)
    else:
        os.remove(path)


def create_dirpath(depth: int = 1) -> str:
    prefix = inspect.currentframe().f_back.f_code.co_name
    path = '/'.join([random_string() for _ in range(depth)])
    dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(dir, f'{prefix}-{path}')
