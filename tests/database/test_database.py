import os
import json
import pytest

from json_as_db import Database
from utils import file, logger


CUR_DIR = os.path.dirname(os.path.realpath(__file__))
DB_FILENAME = 'basic.json'
DB_FILEPATH = os.path.join(CUR_DIR, '..', 'samples', DB_FILENAME)
REC_ID = 'kcbPuqpfV3YSHT8YbECjvh'
REC_ID_2 = 'jmJKBJBAmGESC3rGbSb62T'
REC_ID_NOT_EXIST = 'N0t3xIstKeyV41ueString'


def setup_db() -> Database:
    logger.debug('setup: (file) '+ DB_FILEPATH)

    with open(DB_FILEPATH, 'r') as f:
        data = json.load(f)

    db = Database(data)
    db.__path__ = DB_FILEPATH
    db.__name__ = DB_FILENAME
    return db


@pytest.fixture()
def db() -> Database:
    yield setup_db()


def test_read_db_attributes(db: Database):
    record = db.get(REC_ID)

    assert isinstance(record.get('list'), list)
    assert record.get('booleanTrue') == True
    assert record.get('booleanFalse') == False
    assert record.get('randomInteger') == 123
    assert record.get('randomString') == 'keyboard-cat'
    assert record.get('not-exists-key') == None


def test_db_add(db: Database):
    assert db.count() == 2
    item = {
        'randomInteger': 111,
    }
    new_id = db.add(item)
    assert type(new_id) is str
    assert db.count() == 3

    found = db.get(new_id)
    assert found == item


def test_db_add_many(db: Database):
    assert db.count() == 2
    item_1 = {
        'randomInteger': 111,
    }
    item_2 = {
        'randomInteger': 999,
    }
    new_ids = db.add([item_1, item_2])
    assert type(new_ids) is list
    assert len(new_ids) == 2
    assert db.count() == 4

    assert db.get(new_ids[0]) == item_1
    assert db.get(new_ids[1]) == item_2


def test_db_remove(db: Database):
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


def test_db_remove_by_ids(db: Database):
    db.remove([REC_ID])
    pytest.skip()


def test_db_get_by_id(db: Database):
    found = db.get(REC_ID)
    assert found['randomInteger'] == 123


def test_db_get_by_ids(db: Database):
    found = db.get([REC_ID, REC_ID_2])
    assert found[0]['randomInteger'] == 123
    assert found[1]['randomInteger'] == 321


def test_db_update_by_id(db: Database):
    db.modify(REC_ID, {

    })
    pytest.skip()


def test_db_update_by_ids(db: Database):
    keys = [REC_ID, REC_ID_2]
    values = [
        {

        },
        {

        }
    ]
    db.modify(keys, values)
    pytest.skip()


def test_db_all(db: Database):
    records = db.all()
    logger.debug(records)
    assert len(records) == 2
    cat_names = set(map(lambda rec: rec['randomString'], records))
    expected = set(['keyboard-cat', 'cheshire-cat'])
    assert expected == cat_names


def test_db_clear(db: Database):
    assert db.count() == 2
    db.clear()
    assert db.count() == 0


def test_db_find_by_function(db: Database):
    db.find(lambda x: True)
    pytest.skip()


def test_db_has(db: Database):
    db.has(REC_ID)
    pytest.skip()


def test_db_has(db: Database):
    db.has([REC_ID, REC_ID_2])
    pytest.skip()


def test_db_count(db: Database):
    assert db.count() == 2


def test_db_drop(db: Database):
    dropped_count = db.drop()
    assert dropped_count == 2
    dropped_count = db.drop()
    assert dropped_count == 0


def test_db_commit(db: Database):
    db.commit()
    pytest.skip()


def test_db_rollback(db: Database):
    db.rollback()
    pytest.skip()


@pytest.mark.asyncio
async def test_db_save(db: Database):
    """ await db.save() """
    pytest.skip()

