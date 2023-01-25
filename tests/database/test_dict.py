import os
import pytest

from utils import file, logger, fail

from json_as_db import Database


CUR_DIR = os.path.dirname(os.path.realpath(__file__))
DB_FILENAME = 'db.json'
DB_FILEPATH = os.path.join(CUR_DIR, '..', 'samples', DB_FILENAME)
REC_ID = 'kcbPuqpfV3YSHT8YbECjvh'
REC_ID_2 = 'jmJKBJBAmGESC3rGbSb62T'
REC_ID_NOT_EXIST = 'N0t3xIstKeyV41ueString'
DB_STR_OUTPUT = """booleanFalse  booleanTrue  ...  randomInteger  randomString
False         True         ...  123            keyboard-cat
None          None         ...  321            cheshire-cat


[2 items, 6 keys]"""


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


def test_len(db: Database):
    assert type(len(db)) is int
    assert len(db) == 2


def test_items(db: Database):
    assert type(db.items()) is type(dict().items())


def test_keys(db: Database):
    assert type(db.keys()) is type(dict().keys())


def test_values(db: Database):
    assert type(db.values()) is type(dict().values())


def test_repr(db: Database):
    assert repr(db) == DB_STR_OUTPUT


def test_str(db: Database):
    assert str(db) == DB_STR_OUTPUT


def test_contains(db: Database):
    """The `in` keyword is used to check if a value is present in a sequence (list, range, string etc.).
    """
    assert True == (REC_ID in db)
    assert True == (REC_ID_2 in db)
    assert False == (REC_ID_NOT_EXIST in db)


def test_constructor():
    extenral_dict = dict(age=25, name='Tom')
    try:
        db = Database(extenral_dict)
    except:
        fail()


def test_deconstructor():
    db = Database(dict())
    try:
        del db
    except:
        fail()
