import os
import pytest
import os

from json_as_db import Client
from utils import file


CUR_DIR = os.path.dirname(os.path.realpath(__file__))


def make_path(dirpath: str):
    return os.path.join(CUR_DIR, dirpath)


def test_init_client(client: Client):
    assert client != None


def test_init_client_with_creating_directory():
    dirpath = make_path(file.create_dirpath(prefix='new'))
    assert not os.path.exists(dirpath)

    try:
        client = Client(dirpath)
        assert file.is_dir(dirpath)
    finally:
        file.remove(dirpath)


def test_init_client_with_creating_deep_directory():
    paths = file.create_dirpath(prefix='deep', depth=2)
    first_dir = paths.split(os.path.sep)[0]
    deep_dirpath = make_path(paths)

    try:
        client = Client(deep_dirpath)
        assert file.is_dir(deep_dirpath)
    finally:
        file.remove(make_path(first_dir))


def test_init_client_with_exist_directory():
    dirpath = make_path(file.create_dirpath(prefix='exists'))
    file.mkdirs(dirpath)
    file.touch(os.path.join(dirpath, "somefile1.dat"))
    file.touch(os.path.join(dirpath, "somefile2.txt"))

    try:
        client = Client(dirpath)
        assert file.is_dir(dirpath)
    finally:
        file.remove(dirpath)


def test_init_client_with_wrong_directory():
    dirpath = make_path(file.create_dirpath(prefix='wrong_dir'))
    file.touch(dirpath)

    try:
        client = Client(dirpath)
    except NotADirectoryError:
        assert True
    except:
        pytest.fail()
    finally:
        file.remove(dirpath)
