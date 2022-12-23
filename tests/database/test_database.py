import os
import json
import pytest

from json_as_db import Database
from utils import file, logger


CUR_DIR = os.path.dirname(os.path.realpath(__file__))
DB_FILENAME = 'basic.json'
DB_FILEPATH = os.path.join(CUR_DIR, '..', 'samples', DB_FILENAME)
SAMPLE_REC_ID = 'kcbPuqpfV3YSHT8YbECjvh'


def setup_db() -> Database:
    logger.debug('setup: (file) '+ DB_FILEPATH)

    with open(DB_FILEPATH, 'r') as f:
        data = json.load(f)
        logger.debug('data: '+ str(data))

    db = Database(data)
    db.__path__ = DB_FILEPATH
    db.__name__ = DB_FILENAME
    return db


# def teardown():
#     logger.debug('teardown: (file) '+ DB_FILEPATH)
#     try:
#         file.remove(DB_FILEPATH)
#     except FileNotFoundError:
#         pass


@pytest.fixture()
def db() -> Database:
    yield setup_db()


def test_read_db_attributes(db: Database):
    record = db.get(SAMPLE_REC_ID)

    assert isinstance(record.get('list'), list)
    assert record.get('booleanTrue') == True
    assert record.get('booleanFalse') == False
    assert record.get('randomInteger') == 123
    assert record.get('randomString') == 'keyboard-cat'
    assert record.get('not-exists-key') == None


def test_db_add_by_id(db: Database):
    """ db.add({...}) """
    pass


def test_db_add_by_list(db: Database):
    """ db.add([{...}, {...}]) """
    pass


def test_db_remove_by_id(db: Database):
    """ db.remove(id) """
    pass


def test_db_remove_by_list(db: Database):
    """ db.remove([id]) """
    pass


def test_db_get_by_id(db: Database):
    """ db.get(id) """
    pass


def test_db_get_by_list(db: Database):
    """ db.get([id]) """
    pass


def test_db_update_by_id(db: Database):
    """ db.update(id, {}) """
    pass


def test_db_update_by_list(db: Database):
    """ db.update([id, id], [{...}, {...}]) """
    pass


def test_db_find_by_function(db: Database):
    """ db.find(func) """
    pass


def test_db_has(db: Database):
    """ db.has(id) """
    pass


def test_db_has_by_function(db: Database):
    """ db.has(func) """
    pass


def test_db_drop(db: Database):
    """ db.drop() """
    pass


def test_db_commit(db: Database):
    """ db.commit() """
    pass


def test_db_rollback(db: Database):
    """ db.rollback() """
    pass


@pytest.mark.asyncio
async def test_db_save(db: Database):
    """ await db.save() """
    pass

