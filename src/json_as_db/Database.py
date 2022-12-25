import json
import copy
import shortuuid
import aiofiles

from datetime import datetime
from typing import Any, Union, List, Callable, Tuple
from .constants import package_name

__all__ = ['Database']

_defaults_save_file_kwargs = dict(
    mode="w",
    encoding="utf-8",
)
_defaults_save_json_kwargs = dict(
    sort_keys=True,
)


def _from_maybe_list(value: Union[Any, List[Any]]) -> Tuple[type, List[Any]]:
    return_type = type(value)
    if not isinstance(value, list):
        value = [value]
    return (return_type, value)


def _return_maybe(_type: type, _values: List[Any]) -> Union[Any, List[Any]]:
    if _type is list:
        return _values
    else:
        return _values[0]


def _override_only_unset(__dict: dict, __target: dict):
    unset_fields = set(__target.keys()) - set(__dict.keys())
    new_target = dict()
    for field in unset_fields:
        new_target[field] = __target[field]
    new_dict = copy.deepcopy(__dict)
    new_dict.update(new_target)
    return new_dict


class Database(dict):
    __path__: str
    __name__: str
    __data__ = 'data'
    __version__ = '1.0.0'
    __metadata__ = [
        'version',
        'creator',
        'created_at',
        'updated_at',
    ]
    __memory__ = dict()

    def __init__(self, *arg, **kwargs):
        self.__dict__ = dict(*arg, **kwargs)
        now = datetime.now().isoformat()
        defaults = {
            'version': self.__version__,
            'creator': package_name,
            'created_at': now,
            'updated_at': now,
            # self.__data__: dict(*arg, **kwargs),
            self.__data__: dict(),
        }
        self.__dict__ = _override_only_unset(self.__dict__, defaults)
        self.commit()

    def __getitem__(self, key: str) -> Any:
        try:
            return self.data.__getitem__(key)
        except KeyError:
            return None

    def __setitem__(self, key, value) -> None:
        raise NotImplementedError('Can not set attributes directly')

    def __delitem__(self, key) -> None:
        try:
            self._update_timestamp()
            return self.data.__delitem__(key)
        except KeyError:
            return None

    def __contains__(self, key, **kwargs) -> bool:
        return self.data.__contains__(key, **kwargs)

    def __exports_only_publics(self) -> dict:
        d = self.__dict__
        out = copy.deepcopy(d)
        hidden_keys = list(filter(lambda i: i.startswith('__'), d.keys()))
        for key in hidden_keys:
            out.pop(key)
        return out

    def __repr__(self):
        return self.__exports_only_publics().__repr__()

    def __str__(self):
        return str(self.__repr__())

    def __len__(self):
        return len(self.data)

    def keys(self) -> list:
        return self.data.keys()

    def values(self) -> list:
        return self.data.values()

    @property
    def data(self) -> dict:
        return self.__dict__.get(self.__data__)

    @property
    def filepath(self) -> str:
        return self.__path__

    @property
    def metadata(self) -> dict:
        meta = dict()
        for column in self.__metadata__:
            meta[column] = self.__dict__.get(column)
        return meta

    def _update_timestamp(self) -> None:
        self.__dict__.update({
            'updated_at': datetime.now().isoformat()
        })

    def get(self, key: Union[str, List[str]], default=None) -> Union[Any, List[Any]]:
        _type, _keys = _from_maybe_list(key)
        values = [self.data.get(k, default) for k in _keys]
        return _return_maybe(_type, values)

    def update(self, mapping: Union[dict, tuple] = (), **kwargs) -> None:
        self._update_timestamp()
        return self.data.update(mapping, **kwargs)

    def modify(
        self,
        id: Union[str, List[str]],
        value: Union[Any, List[Any]]
    ) -> Union[Any, List[Any]]:
        """
        Args:
            id (str | List[str]): id(s) to modify
            value (Any | List[Any]): value(s) to modify

        Raises:
            ValueError: type or length is not matched

        Returns:
            Any | List[Any]: Modified value(s)
        """
        type_id, ids = _from_maybe_list(id)
        type_value, values = _from_maybe_list(value)
        if len(ids) != len(values):
            raise ValueError(
                'Can not match ids and values. please check type and length of them')
        for index in range(len(ids)):
            _id, _value = ids[index], values[index]
            target = dict()
            target[_id] = _value
            self.data.update(target)
        self._update_timestamp()
        return _return_maybe(type_id, values)

    def add(self, item: Union[Any, List[Any]]) -> Union[str, List[str]]:
        _type, _items = _from_maybe_list(item)

        ids = []
        for i in _items:
            uid = shortuuid.uuid()
            self.data[uid] = i
            ids.append(uid)

        self._update_timestamp()
        return _return_maybe(_type, ids)

    def remove(self, key: Union[str, List[str]]) -> Union[str, List[str]]:
        _type, _keys = _from_maybe_list(key)
        popped = [self.data.pop(key) for key in _keys]
        self._update_timestamp()
        return _return_maybe(_type, popped)

    def all(self) -> List[Any]:
        return list(self.data.values())

    def clear(self) -> None:
        self.data.clear()
        self._update_timestamp()

    def find(self, func: Callable[..., bool]) -> List[str]:
        ids = []
        for id, value in self.data.items():
            if func(value):
                ids.append(id)
        return ids

    def has(self, key: Union[str, List[str]]) -> Union[bool, List[bool]]:
        _type, _keys = _from_maybe_list(key)
        key_set = set(self.data.keys())
        values = [k in key_set for k in _keys]
        return _return_maybe(_type, values)

    def count(self) -> int:
        """

        Returns:
            int: indicates the count of all data
        """
        return len(self.data.keys())

    def drop(self) -> int:
        """

        Returns:
            int: indicates the count of dropped items
        """
        del_count = self.count()
        self.data.clear()
        return del_count

    def commit(self) -> None:
        self.__memory__ = copy.deepcopy(self.__dict__)

    def rollback(self) -> None:
        self.__dict__ = copy.deepcopy(self.__memory__)

    async def save(
        self,
        file_kwds: dict = dict(
            mode="w",
            encoding="utf-8",
        ),
        json_kwds: dict = dict(
            sort_keys=True,
        )
    ) -> None:
        """
        Save database into file as JSON format

        Args:
            file_kwargs (dict, optional):
                keyword arguments for file `open(**kwagrs)`.
                Defaults to `(mode="w", encoding="utf-8")`.
            json_kwargs (dict, optional):
                keyword arguments for `json.dumps(**kwargs)`.
                Defaults to `(sort_keys=True)`.
        """
        file_kwds = _override_only_unset(file_kwds, _defaults_save_file_kwargs)
        json_kwds = _override_only_unset(json_kwds, _defaults_save_json_kwargs)

        async with aiofiles.open(self.filepath, **file_kwds) as f:
            dict_out = self.__exports_only_publics()
            await f.write(json.dumps(dict_out, **json_kwds))
