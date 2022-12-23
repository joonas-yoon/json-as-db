import os
import pytest
import os

from json_as_db import Client
from utils import file


def test_init_client(client: Client):
    assert client != None


def test_init_client_with_creating_directory():
    dirpath = file.create_dirpath()
    assert not os.path.exists(dirpath)

    try:
        client = Client(dirpath)
        assert file.is_dir(dirpath)
    finally:
        file.remove(dirpath)


def test_init_client_with_creating_deep_directory():
    deep_dirpath = file.create_dirpath(depth=2)

    try:
        client = Client(deep_dirpath)
        assert file.is_dir(deep_dirpath)
    finally:
        parent_dir = deep_dirpath.split('/')[0]
        file.remove(parent_dir)


def test_init_client_with_exist_directory():
    dirpath = file.create_dirpath()
    file.mkdirs(dirpath)
    file.touch(f"{dirpath}/somefile1.dat")
    file.touch(f"{dirpath}/somefile2.txt")

    try:
        client = Client(dirpath)
        assert file.is_dir(dirpath)
    finally:
        file.remove(dirpath)


def test_init_client_with_wrong_directory():
    dirpath = file.create_dirpath()
    file.touch(dirpath)

    try:
        client = Client(dirpath)
    except FileExistsError:
        assert True
    except:
        pytest.fail()
    finally:
        file.remove(dirpath)
