import json
from typing import Optional, Any, Union, List
import aiofiles

__all__ = ['Database']


class Database(dict):
    __path__: str
    __name__: str
    __columns__ = [
        'version',
        'records',
        'creator',
        'created_at',
        'updated_at',
    ]

    def __init__(self, *arg, **kwargs):
        self.__dict__ = dict(*arg, **kwargs)

    def __getitem__(self, key: str) -> Any:
        try:
            return self.records.__getitem__(key)
        except KeyError:
            return None

    def __setitem__(self, key, value) -> None:
        raise NotImplementedError('Can not set attributes directly')

    def __delitem__(self, key) -> None:
        try:
            return self.records.__delitem__(key)
        except KeyError:
            return None

    def __contains__(self, key, **kwargs) -> bool:
        return self.records.__contains__(key, **kwargs)

    def __repr__(self):
        return self.__dict__.__repr__()

    def __str__(self):
        return str(self.__dict__)

    def keys(self) -> list:
        return self.records.keys()

    def values(self) -> list:
        return self.records.values()

    def get(self, key: Union[str, List[str]], default=None) -> Any:
        if isinstance(key, str):
            return self.records.get(key, default)
        if isinstance(key, list):
            return [self.records.get(k, default) for k in key]
        raise ValueError("Invalid type of key")

    def update(self, mapping=(), **kwargs) -> None:
        return self.records.update(mapping, **kwargs)

    @property
    def records(self):
        return self.__dict__.get('records') or dict()

    @property
    def metadata(self) -> dict:
        meta = dict()
        for column in self.__columns__:
            meta[column] = self.__dict__.get(column)
        return meta

    async def save(self) -> None:
        async with aiofiles.open(self.__path__, mode='w') as f:
            await f.write(json.dumps(self))

