import os

from .Table import Table


class Client:
    """
    The Client object contains settings like directory path
    This provides
        - to create initial JSON file from table name
        - to read table from JSON file
        - to write table into JSON file

    Args:
        dir_path (str): base directory path where file will be in
    """
    def __init__(self, dir_path: str = '.'):
        self.dir_path = os.path.join(dir_path)
        if os.path.exists(self.dir_path):
            if not os.path.isdir(self.dir_path):
                raise FileExistsError(f"{self.dir_path} is not a directory")
        else:
            os.makedirs(self.dir_path, exist_ok=True)


    def create_table(name: str) -> Table:
        return None
