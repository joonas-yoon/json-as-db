import pytest

from json_as_db import Client


@pytest.fixture
def client():
    return Client()


def test_create_file(client: Client):
    assert client != None
