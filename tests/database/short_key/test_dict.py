import os
import pytest

from utils import file, logger, fail

from json_as_db import Database


CUR_DIR = os.path.dirname(os.path.realpath(__file__))
DB_FILENAME = 'db.json'
DB_FILEPATH = os.path.join(CUR_DIR, '..', '..', 'samples', DB_FILENAME)
REC_ID = 'kcbPuq'       # 6 letters key
REC_ID_2 = 'jmJKBJBA'   # 8 letters key, and this works!
REC_ID_NOT_EXIST = 'N0t3xIst'


@pytest.fixture()
def db() -> Database:
    return Database().load(DB_FILEPATH)


def test_getter(db: Database):
    item = db[REC_ID]
    logger.debug(item)
    assert type(item) is dict
    assert item['randomInteger'] == 123
    assert type(db[REC_ID_NOT_EXIST]) is type(None)


def test_getter_by_list(db: Database):
    items = db[[REC_ID, REC_ID_2]]
    logger.debug(items)
    assert type(items) is list
    assert len(items) == 2
    items = db[[REC_ID_NOT_EXIST]]
    assert items == [None]


def test_setter(db: Database):
    assert db[REC_ID]['randomInteger'] == 123
    try:
        db[REC_ID] = {'test': True}
    except NotImplementedError:
        pass
    except:
        fail()


def test_del(db: Database):
    try:
        del db[REC_ID]
    except:
        fail()
    assert db[REC_ID] is None


def test_contains(db: Database):
    """The `in` keyword is used to check if a value is present in a sequence (list, range, string etc.).
    """
    assert True == (REC_ID in db)
    assert True == (REC_ID_2 in db)
    assert False == (REC_ID_NOT_EXIST in db)
