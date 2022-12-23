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


def remove(path: str, ignore: bool = False):
    if not path:
        return None
    try:
        shutil.rmtree(path)
    except NotADirectoryError:
        os.remove(path)
    except FileNotFoundError as err:
        if not ignore:
            raise err


def create_dirpath(prefix: str = '', depth: int = 1) -> str:
    paths = ['_' + random_string() for _ in range(depth)]
    if prefix:
        paths[0] = f"{prefix}{paths[0]}"
    return os.path.join(*paths)
