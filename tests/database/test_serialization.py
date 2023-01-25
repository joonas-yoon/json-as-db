import os
import json

from json_as_db import Database
from utils import file, logger

CUR_DIR = os.path.dirname(os.path.realpath(__file__))


def test_load():
    filepath = os.path.join(CUR_DIR, '..', 'samples', 'db.json')
    filepath = os.path.abspath(filepath)
    logger.debug('setup: (file) '+ filepath)

    db = Database().load(filepath)

    item_expected = {
      "randomInteger": 321,
      "randomString": "cheshire-cat",
      "list": [
        "alice", "in", "wonderland"
      ]
    }
    item = db.get("jmJKBJBAmGESC3rGbSb62T")
    logger.debug(item)

    assert item_expected == item


def test_load_from_list_json():
    filepath = os.path.join(CUR_DIR, '..', 'samples', 'list.json')
    filepath = os.path.abspath(filepath)
    logger.debug('setup: (file) '+ filepath)

    db = Database().load(filepath)
    logger.debug(db)
    assert len(db) == 2

    keys = list(db.keys())
    assert len(keys) == 2

    item1 = db.get(keys[0])
    item2 = db.get(keys[1])

    logger.debug(f"db['{keys[0]}'] = {item1}")
    logger.debug(f"db['{keys[1]}'] = {item2}")

    if 'empty' in item1:
        assert item1["randomInteger"] == 123
        assert item2["randomInteger"] == 321
    else:
        assert item1["randomInteger"] == 321
        assert item2["randomInteger"] == 123


def test_load_from_json():
    filepath = os.path.join(CUR_DIR, '..', 'samples', 'sample1.json')
    filepath = os.path.abspath(filepath)
    logger.debug('setup: (file) '+ filepath)

    db = Database().load(filepath)
    assert len(db) == 1

    items = db.all()
    item = items[0]
    assert type(item) is dict

    assert 'someExtraKey' in item
    assert item['someExtraKey'] == 989347
    assert len(item['items']) == 2


def test_save():
    temp_dir = os.path.relpath(os.path.join(CUR_DIR, 'test_save'))
    try:
        file.remove(temp_dir)
    except FileNotFoundError:
        pass
    logger.debug(temp_dir)

    samples = [
        {"id": "ZoomIn", "label": "Zoom In"},
        {"id": "ZoomOut", "label": "Zoom Out"},
        {"id": "OriginalView", "label": "Original View"},
    ]

    db = Database()
    logger.debug(f'[before adding items] {db}')
    db.add(samples)
    logger.debug(f'[after adding items] {db}')

    filepath = os.path.join(temp_dir, 'db.json')
    filepath = os.path.abspath(filepath)
    logger.debug(f'[saving path] {filepath}')
    kwargs = {
        'file_args': {'encoding': 'utf-8'},
        'json_args': {'indent': 4},
    }
    db.save(filepath, make_dirs=True, **kwargs)

    with open(filepath, 'r', encoding='utf-8') as f:
        saved = json.load(f)
        logger.debug(f'[saved] {saved}')

    assert saved['data'] == db.data

    file.remove(temp_dir)
