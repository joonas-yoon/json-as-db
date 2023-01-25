import os
import json
import pytest

from json_as_db import Database
from utils import file, logger


CUR_DIR = os.path.dirname(os.path.realpath(__file__))
DB_FILENAME = 'db.json'
DB_FILEPATH = os.path.join(CUR_DIR, '..', '..', 'samples', DB_FILENAME)
ID = 'kcbPuq' # 6 letters key
ID_NOT_EXIST = 'N0t3xIst'


@pytest.fixture()
def db() -> Database:
    return Database().load(DB_FILEPATH)


def test_get_item(db: Database):
    found = db[ID]
    assert found['randomInteger'] == 123


def test_get_item_not_exist(db: Database):
    found = db[ID_NOT_EXIST]
    assert found == None

