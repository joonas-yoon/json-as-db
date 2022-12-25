Examples
========

Client
------

Constructor
^^^^^^^^^^^

`Client` manages with root directory where contains JSON files for database.

When given ``root_dir`` as like ``Client(root_dir='path/dir')``, `Client` makes
an empty directory with given path ``path/dir``.

.. code-block:: python

    from json_as_db import Client

    client = Client('path/dir')


Create Database
^^^^^^^^^^^^^^^

The name of database means the name of JSON file. so `Client` creates an empty
file with JSON format: ``path/dir/sample.json``.

The ``create_database`` method returns an instance of `Database` type, and you
can deal with this object just like dictionary.

.. code-block:: python

    >>> await client.create_database('sample')
    {'records': {}, 'creator': 'json_as_db', 'created_at': '2022-12-25T14:23:28.906103', 'version': '1.0.0', 'updated_at': '2022-12-25T14:23:28.906103'}


Get Database from file
^^^^^^^^^^^^^^^^^^^^^^

After create database with the below creating method, using file name as its
database name, you can get it from local JSON formatted file as `Database`
object.

This method reads and opens JSON file from directory where `Client` knows. In
following example, `Client` read the file from ``path/dir/sample.json``.

.. code-block:: python

    >> await client.get_database('sample')
    {'records': {}, 'creator': 'json_as_db', 'created_at': '2022-12-25T14:23:28.906103', 'version': '1.0.0', 'updated_at': '2022-12-25T14:23:28.906103'}


Remove Database
^^^^^^^^^^^^^^^

.. warning::
    Please be aware of that file can not be recovered after running.

To remove local JSON file using `Client`, you can run this ``remove_database``
method.

.. code-block:: python

    client.remove_database('sample')


Database
--------

The `Database` is compatible with dictionary_ where is Python built-in class,
except only for some of setters.

.. _dictionary: https://docs.python.org/3/library/stdtypes.htmldict

So you can use them as dictionary-like. please see the following examples.

Add
^^^

Single item

.. code-block:: python

    >>> db.add({
        "id": 1001,
        "type": "Regular"
    })
    "aT7kM2pW8L7JisSkNjpAhr"


Multiple items

.. code-block:: python

    >>> db.add([
      {
        "id": "1001",
        "type": "Regular"
      },
      {
        "id": "1002",
        "type": "Chocolate"
      },
      {
        "id": "1003",
        "type": "Blueberry"
      },
    ])
    ['FqkmbYFSCRCAHQWydhM69v', 'RUJGcVBFANvNRReXa8U3En', 'F3c3rWpzb3Wh2XYQpoYu9v']


Remove
^^^^^^

Single item

.. code-block:: python

    >>> db.remove("aT7kM2pW8L7JisSkNjpAhr")
    {'id': '1001', 'type': 'Regular'}


Multiple items

.. code-block:: python

    >>> db.remove(["FqkmbYFSCRCAHQWydhM69v", "RUJGcVBFANvNRReXa8U3En"])
    [{'id': '1001', 'type': 'Regular'}, {'id': '1002', 'type': 'Chocolate'}]


Get
^^^

Single item

.. code-block:: python

    >>> db.get("aT7kM2pW8L7JisSkNjpAhr")
    {'id': 1001, 'type': 'Regular'}


Multiple items

.. code-block:: python

    >>> db.get(["FqkmbYFSCRCAHQWydhM69v", "RUJGcVBFANvNRReXa8U3En"])
    [{'id': '1001', 'type': 'Regular'}, {'id': '1002', 'type': 'Chocolate'}]


Modify
^^^^^^

Single item

.. code-block:: python

    >>> db.modify(
        id="FqkmbYFSCRCAHQWydhM69v",
        value={
            "type": "Irregular"
        })
    {'type': 'Irregular'}


Multiple items

.. code-block:: python

    >>> db.modify(
        id=["FqkmbYFSCRCAHQWydhM69v", "RUJGcVBFANvNRReXa8U3En"],
        value=[
            {'type': 'Apple'}, {'type': 'Orange'}
        ])
    [{'type': 'Apple'}, {'type': 'Orange'}]


Find
^^^^

.. code-block:: python

    >>> db.find(lambda x: x['type'].endswith('e'))
    ['2g4kaFAiDBPchz66HNPsZa', 'dpKsCc7evmV7Mxq8ikgY89', 'fewugXnJHosmaXeqbXrLtD']
    >>> db.get(['2g4kaFAiDBPchz66HNPsZa', 'dpKsCc7evmV7Mxq8ikgY89', 'fewugXnJHosmaXeqbXrLtD'])
    [{'id': 1001, 'type': 'Chocolate'}, {'id': 1002, 'type': 'Orange'}, {'id': 1003, 'type': 'Apple'}]


Commit & Rollback
^^^^^^^^^^^^^^^^^

When ``commit()``, it saves its states and all items at that time. Using
``rollback()`` restores all states and items from latest commit. Note that
`Database` supports to store only for a single commit.

.. code-block:: python

    # Show all items before commit
    >> db.all()
    [{'type': 'Orange'}]
    # Commit
    >> db.commit()
    # Add some items after commit
    >> db.add([{'type': 'Apple'}, {'type': 'Banana'}])
    >> db.all()
    [{'type': 'Orange'}, {'type': 'Apple'}, {'type': 'Banana'}]
    # Rollback
    >>> db.rollback()
    >>> db.all()
    [{'type': 'Orange'}]


Save
^^^^

Save `Database` into file as JSON format. You can read from this saved file
by getting methods with `Client` class.

.. code-block:: python

    >>> await db.save()

It supports keyword parameters for JSON formatter and options to file saving.
Please refer to the document page of modules in details

.. code-block:: python

    >>> await db.save(file_kwds={'encoding': 'utf-8'}, json_kwds={'indent': 4})

.. code-block:: json

    {
        "created_at": "2022-12-25T16:50:02.459068",
        "creator": "json_as_db",
        "records": {
            "AwMJDzrjkpWJCee5iSozXW": {
                "type": "Orange"
            }
        },
        "updated_at": "2022-12-25T17:11:56.790276",
        "version": "1.0.0"
    }
