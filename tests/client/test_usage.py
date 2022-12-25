import os
import pytest

from json_as_db import Client
from utils import file, logger

CUR_DIR = os.path.dirname(os.path.realpath(__file__))


def setup_files(root_dir: str):
    logger.debug('setup: '+ root_dir)


def teardown_files(root_dir: str):
    logger.debug('teardown: '+ root_dir)
    try:
        file.remove(root_dir)
    except FileNotFoundError:
        pass


def test_init_and_remove():
    root_dir = os.path.join(CUR_DIR, file.create_dirpath(prefix='test_usage'))

    client = Client(root_dir)
    db = client.create_database('my_database')
    db_get = client.get_database('my_database')
    assert db == db_get
    client.remove_database('my_database')

    teardown_files(root_dir)
