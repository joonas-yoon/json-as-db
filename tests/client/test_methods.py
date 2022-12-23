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
async def test_client_create_empty_table(client: Client):
    table = await client.create_table('table')
    assert isinstance(table, dict)
    path = os.path.join(DB_DIR, 'table.json')
    logger.debug(path)
    assert os.path.exists(path)

    with open(path, 'r') as f:
        # should works without error
        json.load(f)


@pytest.mark.asyncio
async def test_client_create_table(client: Client):
    table = await client.create_table('table')
    assert isinstance(table, dict)
    path = os.path.join(DB_DIR, 'table.json')
    logger.debug(path)
    assert os.path.exists(path)


@pytest.mark.asyncio
async def test_client_create_table_conflict(client: Client):
    path = os.path.join(DB_DIR, 'table.json')
    file.touch(path)
    try:
        table = await client.create_table('table')
    except FileExistsError:
        pass


@pytest.mark.asyncio
async def test_client_get_table(client: Client):
    path = os.path.join(DB_DIR, 'table.json')

    dummy = dict(a=1, b="str", c=False, d=3.14)

    with open(path, 'w') as f:
        json.dump(dummy, f)

    with open(path, 'r') as f:
        answer = json.load(f)

    assert json.dumps(dummy) == json.dumps(answer)

    table = await client.get_table('table')
    assert json.dumps(table) == json.dumps(answer)

