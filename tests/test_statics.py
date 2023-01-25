import os
import json
import pytest
import json_as_db as jad

from utils import file, logger, fail


CUR_DIR = os.path.dirname(os.path.realpath(__file__))
DB_FILENAME = 'db.json'
DB_FILEPATH = os.path.join(CUR_DIR, 'samples', DB_FILENAME)


def test_load_database():
    db = jad.load(DB_FILEPATH)
    assert type(db) is jad.Database


def test_load_database_fail():
    try:
        db = jad.load('./samples/.notexists')
        assert type(db) is jad.Database
    except FileNotFoundError:
        pass
    except:
        fail()
