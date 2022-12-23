import os
import json
import aiofiles


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
                raise NotADirectoryError(f"{self.dir_path} is not a directory")
        else:
            os.makedirs(self.dir_path, exist_ok=True)


    async def create_table(self, name: str, ext: str = 'json') -> dict:
        file_name = name
        if ext:
            file_name += f".{ext}"
        file_path = os.path.join(self.dir_path, file_name)

        if os.path.exists(file_path):
            raise FileExistsError(f"Failed to create file on {file_path}")

        empty_dict = dict()
        async with aiofiles.open(file_path, mode='w') as f:
            await f.write(json.dumps(empty_dict))

        return empty_dict
