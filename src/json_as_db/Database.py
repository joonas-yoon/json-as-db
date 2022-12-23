import json
import shortuuid
import aiofiles

from typing import Any, Union, List, Callable, Tuple

__all__ = ['Database']


def from_maybe_list(value: Union[Any, List[Any]]) -> Tuple[type, List[Any]]:
    return_type = type(value)
    if not isinstance(value, list):
        value = [value]
    return (return_type, value)


def return_maybe(_type: type, _values: List[Any]) -> Union[Any, List[Any]]:
    if _type is list:
        return _values
    else:
        return _values[0]


class Database(dict):
    __path__: str
    __name__: str
    __records__ = 'records'
    __metadata__ = [
        'version',
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

    @property
    def records(self) -> dict:
        return self.__dict__.get(self.__records__) or dict()

    @property
    def filepath(self) -> str:
        return self.__path__

    @property
    def metadata(self) -> dict:
        meta = dict()
        for column in self.__metadata__:
            meta[column] = self.__dict__.get(column)
        return meta

    def get(self, key: Union[str, List[str]], default=None) -> Union[Any, List[Any]]:
        _type, _keys = from_maybe_list(key)
        values = [self.records.get(k, default) for k in _keys]
        return return_maybe(_type, values)

    def update(self, mapping: Union[dict, tuple] = (), **kwargs) -> None:
        return self.records.update(mapping, **kwargs)

    def modify(self, id: Union[str, List[str]], values: Union[Any, List[Any]]) -> None:
        pass

    def add(self, item: Union[Any, List[Any]]) -> Union[str, List[str]]:
        _type, _items = from_maybe_list(item)

        ids = []
        for i in _items:
            uid = shortuuid.uuid()
            self.records[uid] = i
            ids.append(uid)

        return return_maybe(_type, ids)

    def remove(self, key: Union[str, List[str]]) -> Union[str, List[str]]:
        _type, _keys = from_maybe_list(key)
        popped = [self.records.pop(key) for key in _keys]
        return return_maybe(_type, popped)

    def all(self) -> List[Any]:
        return self.records.values()

    def clear(self) -> None:
        self.records.clear()

    def find(self, func: Callable) -> List[str]:
        pass

    def has(self, key: Union[str, List[str]]) -> Union[str, List[str]]:
        pass

    def count(self) -> int:
        """_summary_

        Returns:
            int: indicates the count of all records
        """
        return len(self.records.keys())

    def drop(self) -> int:
        """_summary_

        Returns:
            int: indicates the count of dropped items
        """
        del_count = self.count()
        self.records.clear()
        return del_count

    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass

    async def save(self) -> None:
        async with aiofiles.open(self.filepath, mode='w') as f:
            await f.write(json.dumps(self))

