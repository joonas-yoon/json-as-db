import os
import json
import pytest

from json_as_db import Database
from utils import file, logger


CUR_DIR = os.path.dirname(os.path.realpath(__file__))
DB_FILENAME = 'basic.json'
DB_FILEPATH = os.path.join(CUR_DIR, '..', 'samples', DB_FILENAME)
ID = 'kcbPuqpfV3YSHT8YbECjvh'
ID_NOT_EXIST = 'N0t3xIstKeyV41ueString'


@pytest.fixture()
def db() -> Database:
    return Database().load(DB_FILEPATH)


def test_metadata(db: Database):
    metadata = db.metadata
    assert bool(metadata)
    assert metadata['version'] == '0.0.2b1'
    assert metadata['creator'] == 'json-as-db'
    assert metadata['created_at'] == '2022-12-23T09:17:31.814215'
    assert metadata['updated_at'] == '2022-12-23T15:56:04.586110'


def test_data(db: Database):
    assert db.data[ID] == db.get(ID)
    assert db.data.get(ID) == db.get(ID)


def test_get_item(db: Database):
    found = db[ID]
    assert found['randomInteger'] == 123


def test_get_item_not_exist(db: Database):
    found = db[ID_NOT_EXIST]
    assert found == None

