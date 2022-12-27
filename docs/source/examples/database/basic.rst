Basic operations
================

Add
^^^

You can add single item into `Database`. It returns automatically generated
ID of added item. This new ID is important to use to get and to manipulate
data from `Database`.

.. code-block:: python

    >>> db.add({
    ...     "id": 1001,
    ...     "type": "Regular"
    ... })
    "aT7kM2pW8L7JisSkNjpAhr"


It supports to add multiple items with list.

.. code-block:: python

    >>> db.add([
    ...   {
    ...     "id": "1001",
    ...     "type": "Regular"
    ...   },
    ...   {
    ...     "id": "1002",
    ...     "type": "Chocolate"
    ...   },
    ...   {
    ...     "id": "1003",
    ...     "type": "Blueberry"
    ...   },
    ... ])
    ['FqkmbYFSCRCAHQWydhM69v', 'RUJGcVBFANvNRReXa8U3En', 'F3c3rWpzb3Wh2XYQpoYu9v']


Remove
^^^^^^

You can remove object(s) in `Database` using remove method by given ID(s).
It returns removed object from `Database`.

.. code-block:: python

    >>> db.remove("aT7kM2pW8L7JisSkNjpAhr")
    {'id': '1001', 'type': 'Regular'}
    >>> db.remove(["FqkmbYFSCRCAHQWydhM69v", "RUJGcVBFANvNRReXa8U3En"])
    [{'id': '1001', 'type': 'Regular'}, {'id': '1002', 'type': 'Chocolate'}]


Get
^^^

You can get object(s) by given ID(s) in two ways, the first one is:

.. code-block:: python

    >>> db.get("aT7kM2pW8L7JisSkNjpAhr")
    {'id': '1001', 'type': 'Regular'}
    >>> db.get(["FqkmbYFSCRCAHQWydhM69v", "RUJGcVBFANvNRReXa8U3En"])
    [{'id': '1001', 'type': 'Regular'}, {'id': '1002', 'type': 'Chocolate'}]

The second way, to get a single object with ID, is using getter operation.

.. code-block:: python

    >>> db["aT7kM2pW8L7JisSkNjpAhr"]
    {'id': '1001', 'type': 'Regular'}

If there is no key in `Database` with given ID(s), it returns simply ``None``.

.. code-block:: python

    >>> db.get("NotExistKeyString")
    None
    >>> db.get(['FqkmbYFSCRCAHQWydhM69v', 'NotExistKeyString'])
    [{'id': '1001', 'type': 'Regular'}, None]


Modify
^^^^^^

Single item

.. code-block:: python

    >>> db.modify(
    ...     id="FqkmbYFSCRCAHQWydhM69v",
    ...     value={
    ...         "type": "Irregular"
    ...     })
    {'type': 'Irregular'}


Multiple items

.. code-block:: python

    >>> db.modify(
    ...     id=["FqkmbYFSCRCAHQWydhM69v", "RUJGcVBFANvNRReXa8U3En"],
    ...     value=[
    ...         {'type': 'Apple'}, {'type': 'Orange'}
    ...     ])
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

    >>> db.all()  # Show all items before commit
    [{'type': 'Orange'}]
    >>> db.commit()
    >>> db.add([{'type': 'Apple'}, {'type': 'Banana'}])  # Add some items after commit
    >>> db.all()
    [{'type': 'Orange'}, {'type': 'Apple'}, {'type': 'Banana'}]
    >>> db.rollback()
    >>> db.all()
    [{'type': 'Orange'}]


Load
^^^^

You can get the `Database` object from local JSON formatted file.

This method reads JSON file from directory where given path. In
following example, it reads the file from ``path/dir/sample.json``.

.. code-block:: python

    >>> db.load('path/dir/sample.json')
    {'data': {'2g4kaFAiDBPchz66HNPsZa': {'type': 'Orange'}}, 'creator': 'json_as_db', 'created_at': '2022-12-25T14:23:28.906103', 'version': '1.0.0', 'updated_at': '2022-12-25T14:23:28.906103'}


Save
^^^^

Save `Database` into file as JSON format. You can read from this saved file.

.. code-block:: python

    >>> db.save()

It supports keyword parameters for JSON formatter and options to file saving.
Please refer to the document page of modules in details.

.. code-block:: python

    >>> db.save(file_kwds={'encoding': 'utf-8'}, json_kwds={'indent': 4})

then you can see the file content as like the following,

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
