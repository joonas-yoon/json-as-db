import os
import json
import pytest

from utils import file, logger

from json_as_db import Database, Condition, Key


CUR_DIR = os.path.dirname(os.path.realpath(__file__))
DB_FILENAME = 'db.json'
DB_FILEPATH = os.path.join(CUR_DIR, '..', 'samples', DB_FILENAME)
REC_ID = 'kcbPuqpfV3YSHT8YbECjvh'
REC_ID_2 = 'jmJKBJBAmGESC3rGbSb62T'
REC_ID_NOT_EXIST = 'N0t3xIstKeyV41ueString'


@pytest.fixture()
def db() -> Database:
    return Database().load(DB_FILEPATH)


def test_with_lambda(db: Database):
    result = db.find(lambda v: True)
    assert len(result) == db.count()
    found = db.find(lambda item: item['randomInteger'] == 123)
    assert found == [REC_ID]
    found = db.find(lambda item: 'alice' in item['list'])
    assert found == [REC_ID_2]
    found = db.find(lambda v: False)
    assert found == []
    found = db.find(lambda item: item['randomString'].endswith('cat'))
    assert len(found) == 2
    assert set(found) == set([REC_ID, REC_ID_2])


def test_with_condition_equal(db: Database):
    condition: Condition = Key('randomInteger') == 123
    logger.debug(condition)
    result = db.find(condition)
    assert len(result) == 1
    found = db.get(result[0])
    assert found['randomInteger'] == 123


def test_with_condition_not_equal(db: Database):
    condition: Condition = Key('randomInteger') != 123
    logger.debug(condition)
    result = db.find(condition)
    assert len(result) == 1
    found = db.get(result[0])
    assert found['randomInteger'] == 321

    condition: Condition = Key('randomInteger') != 'stringType'
    logger.debug(condition)
    result = db.find(condition)
    assert len(result) == 2


def test_with_condition_less_than(db: Database):
    condition: Condition = Key('randomInteger') < 200
    logger.debug(condition)
    result = db.find(condition)
    assert len(result) == 1
    found = db.get(result[0])
    assert found['randomInteger'] == 123

    condition: Condition = Key('randomInteger') < 999
    logger.debug(condition)
    result = db.find(condition)
    assert len(result) == 2


def test_with_condition_less_than_equal(db: Database):
    condition: Condition = Key('randomInteger') <= 122
    logger.debug(condition)
    result = db.find(condition)
    assert len(result) == 0

    condition: Condition = Key('randomInteger') <= 123
    logger.debug(condition)
    result = db.find(condition)
    found = db.get(result[0])
    assert found['randomInteger'] == 123


def test_with_condition_greater_than(db: Database):
    condition: Condition = Key('randomInteger') > 200
    logger.debug(condition)
    result = db.find(condition)
    assert len(result) == 1
    found = db.get(result[0])
    assert found['randomInteger'] == 321

    condition: Condition = Key('randomInteger') > 999
    logger.debug(condition)
    result = db.find(condition)
    assert len(result) == 0


def test_with_condition_greater_than_equal(db: Database):
    condition: Condition = Key('randomInteger') >= 123
    logger.debug(condition)
    result = db.find(condition)
    assert len(result) == 2

    condition: Condition = Key('randomInteger') >= 200
    logger.debug(condition)
    result = db.find(condition)
    found = db.get(result[0])
    assert found['randomInteger'] == 321

    condition: Condition = Key('randomInteger') >= 321
    logger.debug(condition)
    result = db.find(condition)
    found = db.get(result[0])
    assert found['randomInteger'] == 321


def test_with_condition_non_exist_key(db: Database):
    condition: Condition = Key('nonExistKey') == 'nothing'
    logger.debug(condition)
    result = db.find(condition)
    assert len(result) == 0


def test_with_condition_and(db: Database):
    condition1: Condition = Key('randomInteger') >= 123
    condition2: Condition = Key('randomInteger') <= 321
    logger.debug(condition1 & condition2)
    result = db.find(condition1 & condition2)
    assert len(result) == 2


def test_with_condition_or(db: Database):
    condition1: Condition = Key('randomInteger') == 123
    condition2: Condition = Key('randomString') == 'cheshire-cat'
    logger.debug(condition1 | condition2)
    result = db.find(condition1 | condition2)
    assert len(result) == 2

    condition1: Condition = Key('randomInteger') == 321
    condition2: Condition = Key('randomString') == 'cheshire-cat'
    logger.debug(condition1 | condition2)
    result = db.find(condition1 | condition2)
    assert len(result) == 1
    found = db.get(result[0])
    assert found['randomInteger'] == 321


def test_with_condition_and_and(db: Database):
    condition1: Condition = Key('randomInteger') == 123
    condition2: Condition = Key('randomString') == 'cheshire-cat'
    condition3: Condition = Key('booleanFalse') == False
    logger.debug(condition1 & condition2 & condition3)
    result = db.find(condition1 & condition2 & condition3)
    logger.debug(result)
    assert len(result) == 0


def test_with_condition_and_or(db: Database):
    condition1: Condition = Key('randomInteger') == 123
    condition2: Condition = Key('randomString') == 'keyboard-cat'
    condition3: Condition = Key('booleanFalse') == None
    logger.debug(condition1 & condition2 | condition3)
    result = db.find(condition1 & condition2 | condition3)
    logger.debug(result)
    assert len(result) == 1

    variant = db.find((condition1 & condition2) | condition3)
    assert variant == result

    variant = db.find(condition2 & condition1 | condition3)
    assert variant == result


def test_with_condition_non_exists(db: Database):
    condition: Condition = Key('empty') == None
    logger.debug(condition)
    result = db.find(condition)
    logger.debug(result)
    assert len(result) == 1


def test_with_condition_not(db: Database):
    condition: Condition = Key('empty') == None
    logger.debug(condition)
    result = db.find(~condition)
    logger.debug(result)
    assert len(result) == 0
