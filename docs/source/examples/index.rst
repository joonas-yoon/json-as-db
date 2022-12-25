Examples
========

.. toctree::
   :maxdepth: 2

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

    >>> await client.get_database('sample')
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

.. toctree::
   :maxdepth: 2
   :glob:

   database/basic
   database/others
   database/specials
