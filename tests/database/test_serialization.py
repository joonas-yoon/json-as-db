import os
import json

from json_as_db import Database
from utils import file, logger

CUR_DIR = os.path.dirname(os.path.realpath(__file__))


def test_db_load() -> Database:
    filepath = os.path.join(CUR_DIR, '..', 'samples', 'basic.json')
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



def test_db_save():
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
