import json

from ..Database import Database
from .BaseClient import BaseClient


class Client(BaseClient):
    """
    The Client object contains settings like directory path
    This provides
    - to create initial JSON file from database name
    - to read database from JSON file
    - to remove linked JSON file with database

    Args:
        dir_path (str): base directory path where file will be in
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_database(self, database_name: str) -> Database:
        file_path = self._ensure_get_filepath(database_name, ensure_exists=False)

        empty_dict = dict()
        with open(file_path, mode='w') as f:
            f.write(json.dumps(empty_dict))

        return self._wrapping_database(empty_dict, database_name)

    def get_database(self, database_name: str) -> Database:
        file_path = self._ensure_get_filepath(database_name, ensure_exists=True)

        with open(file_path, mode='r') as f:
            data = json.loads(f.read())

        print('get_database::data', data)

        return self._wrapping_database(data, database_name)

    def remove_database(self, database_name: str) -> None:
        super().remove_database(database_name)
