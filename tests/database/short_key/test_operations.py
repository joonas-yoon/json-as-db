import os
import json
import pytest

from json_as_db import Database
from utils import file, logger


CUR_DIR = os.path.dirname(os.path.realpath(__file__))
DB_FILENAME = 'db.json'
DB_FILEPATH = os.path.join(CUR_DIR, '..', '..', 'samples', DB_FILENAME)
REC_ID = 'kcbPuq'       # 6 letters key
REC_ID_2 = 'jmJKBJBA'   # 8 letters key, and this works!
REC_ID_NOT_EXIST = 'N0t3xIst'


@pytest.fixture()
def db() -> Database:
    return Database().load(DB_FILEPATH)


def test_remove(db: Database):
    assert db.count() == 2

    try:
        db.remove(REC_ID_NOT_EXIST)
    except KeyError:
        pass

    target = db.get(REC_ID)
    removed = db.remove(REC_ID)
    assert db.count() == 1
    assert removed == target
    assert None == db.get(REC_ID)
    try:
        db.remove(REC_ID)
    except KeyError:
        pass


def test_remove_single_list(db: Database):
    assert db.count() == 2
    target = db.get(REC_ID)
    removed = db.remove([REC_ID])
    assert db.count() == 1
    assert type(removed) is list
    assert removed[0] == target


def test_remove_many(db: Database):
    assert db.count() == 2
    target_1 = db.get(REC_ID)
    target_2 = db.get(REC_ID_2)
    removed = db.remove([REC_ID, REC_ID_2])
    assert db.count() == 0
    assert type(removed) is list
    assert removed[0] == target_1
    assert removed[1] == target_2


def test_get_by_id(db: Database):
    found = db.get(REC_ID)
    assert found['randomInteger'] == 123


def test_get_by_ids(db: Database):
    found = db.get([REC_ID, REC_ID_2])
    assert found[0]['randomInteger'] == 123
    assert found[1]['randomInteger'] == 321


def test_modify_by_id(db: Database):
    target = {
        'newString': 'demian',
    }
    db.modify(REC_ID, target)
    assert db.get(REC_ID) == target


def test_modify_by_ids(db: Database):
    keys = [REC_ID, REC_ID_2]
    values = [
        {
            'nulla': ['non', 'malesuada'],
        },
        {
            'suspendisse': {
                'at': 'nulla quis',
            },
        }
    ]
    db.modify(keys, values)
    assert db.get(keys[0]) == values[0]
    assert db.get(keys[1]) == values[1]


def test_modify_wrong_params(db: Database):
    try:
        # 1 key, 2 values
        db.modify(REC_ID, [{}, {}])
        # 1 key but list, 1 value
        db.modify([REC_ID], {})
        # 2 keys, 1 value in list
        db.modify([REC_ID, REC_ID_2], [{}])
    except ValueError:
        pass


def test_has(db: Database):
    assert db.has(REC_ID) == True
    assert db.has(REC_ID_2) == True
    assert db.has(REC_ID_NOT_EXIST) == False


def test_has_many(db: Database):
    assert db.has([REC_ID, REC_ID_2]) == [True, True]
    assert db.has([REC_ID, REC_ID_NOT_EXIST]) == [True, False]
    assert db.has([REC_ID_NOT_EXIST, REC_ID_2]) == [False, True]

    for has in db.has([REC_ID, REC_ID_NOT_EXIST, REC_ID_2]):
        assert type(has) is bool


def test_commit_and_rollback(db: Database):
    prev = db.all()
    assert len(prev) == 2

    assert db.has([REC_ID, REC_ID_2]) == [True, True]
    db.commit()
    new_id = db.add({'something': 'new'})
    assert db.has(new_id) == True

    db.rollback()
    assert db.has([REC_ID, REC_ID_2, new_id]) == [True, True, False]

