import os
import pytest
import os
import shutil
import random
import inspect

from json_as_db import Client


def random_string(length: int = 8):
    s = "0123456789abcdefghijklmnopqrstuvwxyz"
    return ''.join(random.choices(s, k=length))


def is_dir(path: str) -> bool:
    return os.path.exists(path) and os.path.isdir(path)


def mkdirs(path: str, **kwargs) -> None:
    os.makedirs(path, **kwargs)


def touch(path: str):
    with open(path, 'a'):
        os.utime(path, None)


def remove(path: str):
    if is_dir(path):
        shutil.rmtree(path)
    else:
        os.remove(path)


def create_dirpath(prefix: str = '', depth: int = 1) -> str:
    prefix = inspect.currentframe().f_back.f_code.co_name
    path = '/'.join([random_string() for _ in range(depth)])
    dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(dir, f'{prefix}-{path}')


def test_init_client(client: Client):
    assert client != None


def test_init_client_with_creating_directory():
    dirpath = create_dirpath()
    assert not os.path.exists(dirpath)

    try:
        client = Client(dirpath)
        assert is_dir(dirpath)
    finally:
        remove(dirpath)


def test_init_client_with_creating_deep_directory():
    deep_dirpath = create_dirpath(depth=2)

    try:
        client = Client(deep_dirpath)
        assert is_dir(deep_dirpath)
    finally:
        parent_dir = deep_dirpath.split('/')[0]
        remove(parent_dir)


def test_init_client_with_exist_directory():
    dirpath = create_dirpath()
    mkdirs(dirpath)
    touch(f"{dirpath}/somefile1.dat")
    touch(f"{dirpath}/somefile2.txt")

    try:
        client = Client(dirpath)
        assert is_dir(dirpath)
    finally:
        remove(dirpath)


def test_init_client_with_wrong_directory():
    dirpath = create_dirpath()
    touch(dirpath)

    try:
        client = Client(dirpath)
    except FileExistsError:
        assert True
    except:
        pytest.fail()
    finally:
        remove(dirpath)
