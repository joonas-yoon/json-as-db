# JSON-as-DB

![Python Version Badge] [![RTD](https://readthedocs.org/projects/json-as-db/badge/?version=latest)](https://json-as-db.readthedocs.io/) [![PyTest Badge]](https://github.com/joonas-yoon/json-as-db/actions/workflows/pytest.yml) ![PyPI Version Badge] ![PyPI Download Badge] [![Hits Badge]](#)

Using JSON as very lightweight database

```python
>>> db = Database()
>>> db.load('output.json')   # Load database from file
>>> db.add([{                # Add items what you want to add
...   "id": "1002",
...   "type": "Chocolate"
... })
['FqkmbYFSCRCAHQWydhM69v', 'RUJGcVBFANvNRReXa8U3En']
>>> db.save('output.json', json_kwds={'indent': 4})   # Just save it into file.
```

```js
// output.json
{
    "created_at": "2022-12-25T16:50:02.459068",
    "creator": "json_as_db",
    "data": {
        "FqkmbYFSCRCAHQWydhM69v": {
            "id": "1001",
            "type": "Regular"
        },
        "RUJGcVBFANvNRReXa8U3En": {
            "id": "1002",
            "type": "Chocolate"
        }
    },
    "updated_at": "2022-12-28T16:51:36.276790",
    "version": "1.0.0"
}
```

## Documentation

- Read the Docs - https://json-as-db.readthedocs.io/

## Installation

Installing via pip:

```bash
pip install json-as-db
```

Installing via GitHub repository,

```bash
git clone https://github.com/joonas-yoon/json-as-db.git
pip install -e json-as-db
```

## Contributing

Contributing guidelines can be found [CONTRIBUTING.md](CONTRIBUTING).

Welcome all contributions to the community and feel free to contribute.

## License

Under the MIT license. See the [LICENSE] file for more info.


[Python Version Badge]: https://img.shields.io/pypi/pyversions/json-as-db?style=flat-square
[PyTest Badge]: https://github.com/joonas-yoon/json-as-db/actions/workflows/pytest.yml/badge.svg
[PyPI Version Badge]: https://img.shields.io/pypi/v/json-as-db?style=flat-square
[PyPI Download Badge]: https://img.shields.io/pypi/dm/json-as-db?style=flat-square
[Hits Badge]: https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fjoonas-yoon%2Fjson-as-db
[CONTRIBUTING]: CONTRIBUTING.md
[LICENSE]: LICENSE
