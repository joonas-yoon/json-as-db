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


def test_db_add_by_id(db: Database):
    db.add({

    })
    pass


def test_db_add_by_list(db: Database):
    db.add([{

    }, {

    }])
    pass


def test_db_remove_by_id(db: Database):
    db.remove(REC_ID)
    pass


def test_db_remove_by_list(db: Database):
    db.remove([REC_ID])
    pass


def test_db_get_by_id(db: Database):
    db.get(REC_ID)
    pass


def test_db_get_by_list(db: Database):
    db.get([REC_ID])
    pass


def test_db_update_by_id(db: Database):
    db.modify(REC_ID, {

    })
    pass


def test_db_update_by_list(db: Database):
    keys = [REC_ID, REC_ID_2]
    values = [
        {

        },
        {

        }
    ]
    db.modify(keys, values)
    pass


def test_db_all(db: Database):
    db.all()
    pass


def test_db_find_by_function(db: Database):
    db.find(lambda x: True)
    pass


def test_db_has(db: Database):
    db.has(REC_ID)
    pass


def test_db_has(db: Database):
    db.has([REC_ID, REC_ID])
    pass


def test_db_count(db: Database):
    db.count()
    pass


def test_db_drop(db: Database):
    db.drop()
    pass


def test_db_commit(db: Database):
    db.commit()
    pass


def test_db_rollback(db: Database):
    db.rollback()
    pass


@pytest.mark.asyncio
async def test_db_save(db: Database):
    """ await db.save() """
    pass

