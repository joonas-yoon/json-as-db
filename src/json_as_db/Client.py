import os
import json
import aiofiles


class Client:
    """
    The Client object contains settings like directory path
    This provides
        - to create initial JSON file from table name
        - to read table from JSON file
        - to remove linked JSON file with table

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


    def _get_table_path(self, table_name: str) -> tuple:
        """ returns (file_name, file_path) """
        file_name = f"{table_name}.json"
        file_path = os.path.join(self.root_dir, file_name)
        return (file_name, file_path)


    async def create_table(self, name: str) -> dict:
        """_summary_

        Args:
            name (str): table name

        Raises:
            FileExistsError: when failed to create file with given name

        Returns:
            dict: built-in type of dictionary
        """
        file_name, file_path = self._get_table_path(name)

        if os.path.exists(file_path):
            raise FileExistsError(f"Failed to create file on {file_path}")

        empty_dict = dict()
        async with aiofiles.open(file_path, mode='w') as f:
            await f.write(json.dumps(empty_dict))

        return empty_dict


    async def get_table(self, name: str) -> dict:
        """_summary_

        Args:
            name (str): table name

        Raises:
            FileNotFoundError: when there is no json file which has given name

        Returns:
            dict: built-in type of dictionary
        """
        file_name, file_path = self._get_table_path(name)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Not found json file: {file_path}, please create table first.")

        async with aiofiles.open(file_path, mode='r') as f:
            return json.loads(await f.read())


    def remove_table(self, name: str) -> None:
        """_summary_

        Args:
            name (str): table name

        Raises:
            FileNotFoundError: when there is no json file to remove
        """
        file_name, file_path = self._get_table_path(name)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Not found json file: {file_path}, please create table first.")

        os.remove(file_path)
