Examples
========

.. toctree::
   :maxdepth: 2


Database
--------

The `Database` is compatible with dictionary_ where is Python built-in class,
except only for some of setters.

.. _dictionary: https://docs.python.org/3/library/stdtypes.htmldict

So you can use them as dictionary-like, including useful CRUD methods and more.

.. code-block:: python

    >>> from json_as_db import Database
    >>> db = Database()
    >>> db.add([
    ...   { "id": 1001, "type": "Regular" },
    ...   { "id": 1002, "type": "Chocolate" }
    ... ])
    ["aT7kM2pW8L7JisSkNjpAhr", "RUJGcVBFANvNRReXa8U3En"]
    >>> db.get("aT7kM2pW8L7JisSkNjpAhr")
    {"id": 1001, "type": "Regular"}
    >>> db.count()
    2
    >>> db.all()
    [{"id": 1001, "type": "Regular"}, {"id": 1002, "type": "Chocolate"}]
    >>> db.save('path/dir/file.json')


Moreover, `Database` provides and supports many operations.
Please see the following examples.

.. toctree::
   :maxdepth: 2
   :glob:

   database/basic
   database/others
   database/specials
