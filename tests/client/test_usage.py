import pytest

from json_as_db import Client


@pytest.mark.asyncio
async def test_basic_usage():
    client = Client('db')
    table = await client.create_table('my_table')
    table.update({
      'random-integer': 123,
      'random-string': 'keyboard-cat',
      'boolean-true': True,
      'boolean-false': False,
      'empty': None,
      'list': [
          'first element'
      ]
    })
    await client.get_table('my_table')
    client.remove_table('my_table')
