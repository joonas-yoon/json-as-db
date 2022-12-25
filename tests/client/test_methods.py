import os
import json
import pytest
import aiofiles

from json_as_db import Client
from utils import file, logger


CUR_DIR = os.path.dirname(os.path.realpath(__file__))
DB_DIR = os.path.join(CUR_DIR, file.create_dirpath(prefix='test_methods'))


def setup_client():
    logger.debug('setup: '+ DB_DIR)
    file.mkdirs(DB_DIR, exist_ok=True)
    return Client(DB_DIR)


def teardown_client():
    logger.debug('teardown: '+ DB_DIR)
    try:
        file.remove(DB_DIR)
    except FileNotFoundError:
        pass


@pytest.fixture()
def client() -> Client:
    yield setup_client()
    teardown_client()


def test_client_create_empty_database(client: Client):
    database = client.create_database('database')
    assert isinstance(database, dict)
    path = os.path.join(DB_DIR, 'database.json')
    logger.debug(path)
    assert os.path.exists(path)

    with open(path, 'r') as f:
        # should works without error
        json.load(f)


def test_client_create_database(client: Client):
    database = client.create_database('database')
    assert isinstance(database, dict)
    path = os.path.join(DB_DIR, 'database.json')
    logger.debug(path)
    assert os.path.exists(path)


def test_client_create_database_conflict(client: Client):
    path = os.path.join(DB_DIR, 'database.json')
    file.touch(path)
    try:
        database = client.create_database('database')
    except FileExistsError:
        pass


@pytest.mark.asyncio
async def test_client_get_database():
    SAMPLE_DIR = os.path.join(CUR_DIR, '..', 'samples')

    client = Client(SAMPLE_DIR)

    path = os.path.join(SAMPLE_DIR, 'basic.json')

    expected = {
      "randomInteger": 321,
      "randomString": "cheshire-cat",
      "list": [
        "alice", "in", "wonderland"
      ]
    }

    async with aiofiles.open(path, 'r') as f:
        answer = json.loads(await f.read())
        logger.debug(answer)

    assert expected == answer['data']['jmJKBJBAmGESC3rGbSb62T']

    database = client.get_database('basic')
    logger.debug(expected)
    logger.debug(database)
    assert expected == database['jmJKBJBAmGESC3rGbSb62T']

