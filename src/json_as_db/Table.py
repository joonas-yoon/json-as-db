import json
import aiofiles


class Table(dict):
    __path__: str
    __name__: str


    def __init__(self, *arg, **kwargs):
        super(Table, self).__init__(*arg, **kwargs)


    async def save(self) -> None:
        async with aiofiles.open(self.__path__, mode='w') as f:
            await f.write(json.dumps(self))

