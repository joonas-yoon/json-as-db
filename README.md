# JSON-as-DB

![Python Version Badge] [![RTD](https://readthedocs.org/projects/json-as-db/badge/?version=latest)](https://json-as-db.readthedocs.io/) [![PyTest Badge]](https://github.com/joonas-yoon/json-as-db/actions/workflows/pytest.yml) ![PyPI Version Badge] ![PyPI Download Badge] [![Hits Badge]](#)

Using JSON as very lightweight database

## Overview

```python
import json_as_db as jad

db = jad.Database()      # Declare an instance
db.load('output.json')   # Load database from file (optional)
db.add([{                # Add items what you want to add
  "id": "1002",
  "type": "Chocolate"
})
# ['FqkmbYFSCRCAHQWydhM69v', 'RUJGcVBFANvNRReXa8U3En']
```

```python
db[db.find(jad.Key('type') == 'Chocolate')]
# { "id": "1002", "type": "Chocolate" }
```

```python
db.save('output.json', json_kwds={'indent': 4})   # Just save it into file.
"""
file: output.json
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
    "version": "0.2.4"
}
"""
```

```python
print(db)
"""
id    type
1002  Chocolate
1001  Regular


[2 items, 2 keys]
"""
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

## Benchmark

||json_as_db|pandas|
|:-|-:|-:|
|_Loads from file_|`149.11810 ms`|`153.71676 ms`|
|_Appending data_|`8.96103 ms`|`2760.27654 ms`|
|_Searching items_|`9.87914 ms`|`2.59354 ms`|

Please see the details on [BENCHMARK](BENCHMARK.md).

## Contributing

Contributing guidelines can be found [CONTRIBUTING](CONTRIBUTING.md).

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
