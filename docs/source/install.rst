Installation
============

Installing JSON-as-DB is pretty simple.

.. note::
    Using a virtual environment will make the installation easier,
    and will help to avoid clutter in your system-wide libraries.

JSON-as-DB is available on Pypi as ``json-as-db``, so you can install using
pip as like following command.

.. prompt:: bash
    :prompts: $

    pip install json-as-db


Also you can install directly from source. You will need git in order to
clone the repository.

.. prompt:: bash
    :prompts: $

    git clone https://github.com/joonas-yoon/json-as-db.git
    cd json-as-db
    pip install -r src/requirements.txt
    pip install -e src


If you want to test methods working well, here is the unit tests in ``tests/``
directory. These unittest-based tests are written using PyTest_.

.. _PyTest: https://docs.pytest.org/

Now that you have installed all dependencies, you can run tests to check
functions like,

.. prompt:: bash
    :prompts: $

    PYTHONPATH=src python -m pytest
