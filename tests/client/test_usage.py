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


@pytest.mark.asyncio
async def test_basic_usage():
    root_dir = os.path.join(CUR_DIR, file.create_dirpath(prefix='test_usage'))

    client = Client(root_dir)
    database = await client.create_database('my_database')
    database2 = await client.get_database('my_database')
    client.remove_database('my_database')

    teardown_files(root_dir)
