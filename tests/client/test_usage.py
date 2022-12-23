import pytest

from json_as_db import Client


@pytest.mark.asyncio
async def test_basic_usage():
    client = Client('db')
    database = await client.create_database('my_database')
    database.update({
      'random-integer': 123,
      'random-string': 'keyboard-cat',
      'boolean-true': True,
      'boolean-false': False,
      'empty': None,
      'list': [
          'first element'
      ]
    })
    await client.get_database('my_database')
    client.remove_database('my_database')
