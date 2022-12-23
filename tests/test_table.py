import os
import json
import pytest

from json_as_db import Table
from utils import file, logger


CUR_DIR = os.path.dirname(os.path.realpath(__file__))
TABLE_DIR = os.path.join(CUR_DIR, file.create_dirpath(prefix='test_table'))
TABLE_FILE = os.path.join(TABLE_DIR, 'test.json')


def setup():
    logger.debug('setup: '+ TABLE_DIR)
    file.mkdirs(TABLE_DIR, exist_ok=True)
    with open(TABLE_FILE, 'w') as f:
        data = dict(
          randomInteger = 123,
          randomString = 'keyboard-cat',
          booleanTrue = True,
          booleanFalse = False,
          empty = None,
          list = [
              'first element'
          ]
        )
        json.dump(data, f)


def setup_table() -> Table:
    with open(TABLE_FILE, 'r') as f:
        data = json.load(f)

    table = Table(data)
    table.__path__ = TABLE_FILE
    table.__name__ = 'test.json'
    return table


def teardown():
    logger.debug('teardown: (dir) '+ TABLE_DIR)
    logger.debug('teardown: (file) '+ TABLE_FILE)
    try:
        file.remove(TABLE_DIR)
    except FileNotFoundError:
        pass


@pytest.fixture()
def table() -> Table:
    yield setup_table()


def test_read_table_attributes(table: Table):
    assert isinstance(table.get('list'), list)
    assert table.get('booleanTrue') == True
    assert table.get('booleanFalse') == False
    assert table.get('randomInteger') == 123
    assert table.get('randomString') == 'keyboard-cat'
    assert table.get('not-exists-key') == None


@pytest.mark.asyncio
async def test_save_table(table: Table):
    assert table != None
    await table.save()
