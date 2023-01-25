import os
import pytest

from json_as_db import Database
from utils import file, logger


CUR_DIR = os.path.dirname(os.path.realpath(__file__))
DB_FILENAME = 'db.json'
DB_FILEPATH = os.path.join(CUR_DIR, '..', 'samples', DB_FILENAME)
ID = 'kcbPuqpfV3YSHT8YbECjvh'
ID_NOT_EXIST = 'N0t3xIstKeyV41ueString'


@pytest.fixture()
def db() -> Database:
    return Database().load(DB_FILEPATH)


def test_version(db: Database):
    assert type(db.version) == str
    assert db.version == '0.2.4'


def test_data(db: Database):
    assert type(db.data) == dict
    assert db.data[ID]['randomInteger'] == 123


def test_data_equals(db: Database):
    assert db.data[ID] == db.get(ID)
    assert db.data.get(ID) == db.get(ID)


def test_metadata(db: Database):
    assert type(db.metadata) == dict
    assert db.metadata['version'] == '0.2.4'
    assert db.metadata['creator'] == 'json-as-db'
    assert db.metadata['created_at'] == '2022-12-23T09:17:31.814215'
    assert db.metadata['updated_at'] == '2022-12-23T15:56:04.586110'
