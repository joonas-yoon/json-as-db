Examples
========

Client
------

Constructor
^^^^^^^^^^^

`Client` manages with root directory where contains JSON files for database.

.. code-block:: python

    from json_as_db import Client

    client = Client('path/dir')


Create Database
^^^^^^^^^^^^^^^

.. code-block:: python

    db = await client.create_database('sample')


Read Database from file
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    db = await client.get_database('sample')


Delete Database
^^^^^^^^^^^^^^^

.. code-block:: python

    client.remove_database('sample')


Database
--------

The `Database` is compatible with dictionary_ where is Python built-in class,
except only for some of setters.

.. _dictionary: https://docs.python.org/3/library/stdtypes.htmldict

So you can use them as ``dict``-like. please see the following examples.

Add
^^^

Single item

.. code-block:: python

    db.add({
        "id": "1001",
        "type": "Regular"
    })


Multiple items

.. code-block:: python

    db.add([
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


Remove
^^^^^^

Single item

.. code-block:: python

    db.remove(

    )


Multiple items

.. code-block:: python

    db.remove(

    )


Get
^^^

Single item

.. code-block:: python

    db.get(

    )


Multiple items

.. code-block:: python

    db.get(

    )


Modify
^^^^^^

Single item

.. code-block:: python

    TBD


Multiple items

.. code-block:: python

    TBD


Find
^^^^

Single item

.. code-block:: python

    TBD


Multiple items

.. code-block:: python

    TBD


Transaction
^^^^^^^^^^^

Commit

.. code-block:: python

    TBD


Rollback

.. code-block:: python

    TBD


Save
^^^^

.. code-block:: python

    TBD



