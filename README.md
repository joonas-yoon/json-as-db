<div align="center">

<h1>JSON as DB</h1>

<img alt="PyPI Version Badge" src="https://img.shields.io/pypi/v/json-as-db?style=flat-square" />
<img alt="Python Version Badge" src="https://img.shields.io/pypi/pyversions/json-as-db?style=flat-square" />
<a href="https://json-as-db.readthedocs.io/">
  <img alt="Read The Docs" src="https://readthedocs.org/projects/json-as-db/badge/?version=latest" /></a>
<a href="https://github.com/joonas-yoon/json-as-db/actions/workflows/pytest.yml">
  <img alt="PyTest Badge" src="https://github.com/joonas-yoon/json-as-db/actions/workflows/pytest.yml/badge.svg" /></a>

</div>

---

**Documentation**: [https://json-as-db.readthedocs.io/](https://json-as-db.readthedocs.io/)

---

Using JSON as very lightweight database.
Work with JSON-like object for your database operations.

**Major Features:**

- **Simple**: define your model by typing your fields using python types, build queries
  using python comparison operators

- **Developer experience**: field/method autocompletion, type hints, data validation,
  perform database operations with a functional API

- **Fully typed**: leverage static analysis to reduce runtime issues

- **Serialization**: built in JSON serialization and JSON schema generation

- **Pure python implementation**: No external dependencies of packages,
  except only for `shortuuid` to create to safe and unique ID

## Quick Installation

Installing via pip:

```bash
pip install json-as-db
```

## Examples

Load database from JSON file by its path, and then adding any object into database.

```python
>>> import json_as_db as jad
>>> db = jad.Database()      # Declare an instance
>>> db.load('output.json')   # Load database from file (optional)
>>> db.add([{                # Add items what you want to add
...   "id": "1002",
...   "type": "Chocolate"
... })
['FqkmbYFSCRCAHQWydhM69v', 'RUJGcVBFANvNRReXa8U3En']
```

Find any in database with query-like parameters.

```python
>>> from json_as_db import Key
>>> db[db.find(Key('type') == 'Chocolate')]
{ "id": "1002", "type": "Chocolate" }
```

```python
>>> db[db.find((Key('age') > 25) & (Key('name') == 'Charles'))]
[{ "age": 33, "name": "Charles", "job": "Locksmith" }, { "age": 26, ... } ]
```

Save database into file as JSON format. You can read from this saved file.
It supports keyword parameters for JSON formatter and options to file saving.

```python
>>> db.save('output.json', json_args={'indent': 4}, file_args={'encoding': 'utf-8'})
"""
The following contents from file: output.json
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

Represents database as follows in a table visualization.

```python
>>> print(db)
age  grouped  ...  job                name
32   True     ...  Camera operator    Layne
17   False    ...  Flying instructor  Somerled
9    True     ...  Inventor           Joon-Ho
...  ...      ...  ...                ...
23   None     ...  Publican           Melanie
54   True     ...  Racing driver      Eike
41   None     ...  Barrister          Tanja


[100 items, 9 keys]
```

## Benchmark

|(avg. time per operation with 10K items)|json_as_db|pandas|
|:-|-:|-:|
|_Loads from file_|`149.11810 ms`|`153.71676 ms`|
|_Append items_|`8.96103 ms`|`2760.27654 ms`|
|_Search a item_|`9.87914 ms`|`2.59354 ms`|
|_Get an item by key_|`0.0039 ms`|`0.0689 ms`|
|_Updating a item_|`0.0074 ms`|`0.0148 ms`|
|_Updating 5 items in a row_|`0.0130 ms`|`0.9432 ms`|
|_Remove an item_|`0.0012 ms`|`6.0930 ms`|

Please see the details on [BENCHMARK](BENCHMARK.md).

## Contributing

Contributing guidelines can be found [CONTRIBUTING](CONTRIBUTING.md).

Welcome all contributions to the community and feel free to contribute.

## License

Under the MIT license. See the [LICENSE] file for more info.

---

<div align="center">
  <img alt="PyPI Download Badge" src="https://img.shields.io/pypi/dm/json-as-db?style=flat-square" />
  <img alt="Hits Badge" src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fjoonas-yoon%2Fjson-as-db" />
</div>

[Python Version Badge]: https://img.shields.io/pypi/pyversions/json-as-db?style=flat-square
[PyTest Badge]: https://github.com/joonas-yoon/json-as-db/actions/workflows/pytest.yml/badge.svg
[PyPI Version Badge]: https://img.shields.io/pypi/v/json-as-db?style=flat-square
[PyPI Download Badge]: https://img.shields.io/pypi/dm/json-as-db?style=flat-square
[Hits Badge]: https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fjoonas-yoon%2Fjson-as-db
[CONTRIBUTING]: CONTRIBUTING.md
[LICENSE]: LICENSE
