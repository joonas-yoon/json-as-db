import os
import json
import pytest

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


@pytest.mark.asyncio
async def test_client_create_empty_database(client: Client):
    database = await client.create_database('database')
    assert isinstance(database, dict)
    path = os.path.join(DB_DIR, 'database.json')
    logger.debug(path)
    assert os.path.exists(path)

    with open(path, 'r') as f:
        # should works without error
        json.load(f)


@pytest.mark.asyncio
async def test_client_create_database(client: Client):
    database = await client.create_database('database')
    assert isinstance(database, dict)
    path = os.path.join(DB_DIR, 'database.json')
    logger.debug(path)
    assert os.path.exists(path)


@pytest.mark.asyncio
async def test_client_create_database_conflict(client: Client):
    path = os.path.join(DB_DIR, 'database.json')
    file.touch(path)
    try:
        database = await client.create_database('database')
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

    with open(path, 'r') as f:
        answer = json.load(f)

    assert expected == answer['records']['jmJKBJBAmGESC3rGbSb62T']

    database = await client.get_database('basic')
    assert expected == database['jmJKBJBAmGESC3rGbSb62T']

