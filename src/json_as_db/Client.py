import os
import json
import aiofiles

from .Database import Database


class Client:
    """
    The Client object contains settings like directory path
    This provides
        - to create initial JSON file from database name
        - to read database from JSON file
        - to remove linked JSON file with database

    Args:
        dir_path (str): base directory path where file will be in
    """
    def __init__(self, root_dir: str = '.'):
        self.root_dir = os.path.join(root_dir)
        if os.path.exists(self.root_dir):
            if not os.path.isdir(self.root_dir):
                raise NotADirectoryError(f"{self.root_dir} is not a directory")
        else:
            os.makedirs(self.root_dir, exist_ok=True)


    def _get_database_path(self, database_name: str) -> tuple:
        """ returns (file_name, file_path) """
        file_name = f"{database_name}.json"
        file_path = os.path.join(self.root_dir, file_name)
        return (file_name, file_path)


    def _wrapping_database(self, _dict: dict, file_name: str) -> Database:
        database = Database(_dict)
        file_name, file_path = self._get_database_path(file_name)
        database.__path__ = file_path
        database.__name__ = file_name
        return database


    async def create_database(self, database_name: str) -> Database:
        """_summary_

        Args:
            database_name (str): database name

        Raises:
            FileExistsError: when failed to create file with given name

        Returns:
            dict: built-in type of dictionary
        """
        file_name, file_path = self._get_database_path(database_name)

        if os.path.exists(file_path):
            raise FileExistsError(f"Failed to create file on {file_path}")

        empty_dict = dict()
        async with aiofiles.open(file_path, mode='w') as f:
            await f.write(json.dumps(empty_dict))

        return self._wrapping_database(empty_dict, database_name)


    async def get_database(self, database_name: str) -> Database:
        """_summary_

        Args:
            database_name (str): database name

        Raises:
            FileNotFoundError: when there is no json file which has given name

        Returns:
            dict: built-in type of dictionary
        """
        file_name, file_path = self._get_database_path(database_name)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Not found json file: {file_path}, please create database first.")

        async with aiofiles.open(file_path, mode='r') as f:
            data = json.loads(await f.read())

        return self._wrapping_database(data, database_name)


    def remove_database(self, database_name: str) -> None:
        """_summary_

        Args:
            database_name (str): database name

        Raises:
            FileNotFoundError: when there is no json file to remove
        """
        file_name, file_path = self._get_database_path(database_name)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Not found json file: {file_path}, please create database first.")

        os.remove(file_path)
