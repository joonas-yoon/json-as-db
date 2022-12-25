Other operations
================

All
^^^

We can get all values of items in `Database` without their keys.

.. code-block:: python

    >>> db.all()
    [{'type': 'Yogurt'}, {'type': 'Apple'}, {'type': 'Banana'}]

Clear
^^^^^

The clear method removes all of the objects.

.. code-block:: python

    >>> db.clear()

Has
^^^

If we want to know whether `Database` has key, here is easy way to know.
Please see the following examples.

.. code-block:: python

    >>> db.keys()
    dict_keys(['AwMJDzrjkpWJCee5iSozXW', '5C8SJM54ogkCmsNJA2Cdja', '8LEJS5uGuopxcPQ3uKN8ty'])
    >>> db.has('AwMJDzrjkpWJCee5iSozXW')
    True
    >>> db.has('NotExistsKeyString')
    False

And it supports the parameter of list type as it will return list of each
result as boolean.

.. code-block:: python

    >>> db.has(['AwMJDzrjkpWJCee5iSozXW', 'NotExistsKeyString'])
    [True, False]

Count
^^^^^

.. code-block:: python

    >>> db.count()
    3

.. code-block:: python

    >>> len(db)
    3

Drop
^^^^

This works as same as ``clear()`` method, but this returns the count of
dropped items. As you know, the count of dropped one is exactly equal to
the count using ``count()`` before dropping.

.. code-block:: python

    >>> db.all()
    [{'type': 'Yogurt'}, {'type': 'Apple'}, {'type': 'Banana'}]
    >>> db.drop()
    3
    >>> db.all()
    []
    >>> db.drop()
    0

