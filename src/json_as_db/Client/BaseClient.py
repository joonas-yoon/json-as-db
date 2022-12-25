import os
from abc import ABCMeta, abstractmethod

from typing import Tuple
from ..Database import Database


class BaseClient(metaclass=ABCMeta):
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

    def _get_database_path(self, database_name: str) -> Tuple[str, str]:
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

    def _ensure_get_filepath(self, database_name: str, ensure_exists: bool = True) -> str:
        file_name, file_path = self._get_database_path(database_name)

        exists = os.path.exists(file_path)
        if ensure_exists != exists:
            if not exists:
                raise FileNotFoundError(
                    f"Not found json file: {file_path}, please create database first.")
            else:
                raise FileExistsError(f"Failed to create file on {file_path}")

        return file_path

    @abstractmethod
    def create_database(self, database_name: str) -> Database:
        """

        Args:
            database_name (str): database name

        Raises:
            FileExistsError: when failed to create file with given name

        Returns:
            dict: built-in type of dictionary
        """
        pass

    @abstractmethod
    def get_database(self, database_name: str) -> Database:
        """

        Args:
            database_name (str): database name

        Raises:
            FileNotFoundError: when there is no json file which has given name

        Returns:
            dict: built-in type of dictionary
        """
        pass

    def remove_database(self, database_name: str) -> None:
        """

        Args:
            database_name (str): database name

        Raises:
            FileNotFoundError: when there is no json file to remove
        """
        file_path = self._ensure_get_filepath(database_name, ensure_exists=True)
        os.remove(file_path)

