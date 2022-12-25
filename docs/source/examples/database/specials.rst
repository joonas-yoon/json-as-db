Specials
========

Fields
------

Metadata
^^^^^^^^

Retrieves metadata from `Database`. This doesn't contain hidden fields in
instance of its.

.. code-block:: python

    >>> db.metadata
    {'version': '1.0.0', 'creator': 'json_as_db', 'created_at': '2022-12-25T16:50:02.459068', 'updated_at': '2022-12-25T17:11:56.790276'}

Data
^^^^

The ``data`` field is shortcut to get all items directly in code. It returns
all key and values as the following,

.. code-block:: python

    >>> db.data
    {'AwMJDzrjkpWJCee5iSozXW': {'type': 'Orange'}, '5C8SJM54ogkCmsNJA2Cdja': {'type': 'Apple'}, '8LEJS5uGuopxcPQ3uKN8ty': {'type': 'Banana'}}

To keep data in safe, actions to set directly is prohibited. So, when you try
to set it using syntax like ``db.data = {}``, it will fail with `AttributeError`
exception.

.. code-block:: python

    >>> db.data = {'NewInjectedIdWhatIWant': {'type': 'Bug'}}
    AttributeError: can't set attribute


Version
^^^^^^^

.. note::
    This does NOT mean the version of package. This is `Database` version for
    specification to read and parse.

.. code-block:: python

    >>> db.version
    '1.0.0'

Accessor
--------

Dictionary-like
^^^^^^^^^^^^^^^

`Database` object is compatible with `dictionary` which is Python built-in class.

All accessors are wrapped and it provides internal data, not metadata.
Please check the following example runnings and results.

.. code-block:: python

    >>> db.data
    {'AwMJDzrjkpWJCee5iSozXW': {'type': 'Orange'}, '5C8SJM54ogkCmsNJA2Cdja': {'type': 'Apple'}}
    >>> ID = 'AwMJDzrjkpWJCee5iSozXW'
    >>> db.data[ID]
    {'type': 'Orange'}
    >>> db[ID]
    {'type': 'Orange'}
    >>> db.get(ID)
    {'type': 'Orange'}
    >>> db.get(ID).update({'type': 'Yogurt'})
    >>> db.data
    {'AwMJDzrjkpWJCee5iSozXW': {'type': 'Yogurt'}, '5C8SJM54ogkCmsNJA2Cdja': {'type': 'Apple'}}

