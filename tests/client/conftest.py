import pytest

from json_as_db import Client


@pytest.fixture()
def client() -> Client:
    return Client()
