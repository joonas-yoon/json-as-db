import os
import json
import copy
import shortuuid

from datetime import datetime
from typing import Any, Union, List, Callable

from ..constants import package_name, __version__
from .._utils import override_dict, from_maybe_list, return_maybe, decorater
from ._formatting import stringify

__all__ = [
    'Database'
]


class Database(dict):
    __data__ = 'data'
    __metadata__ = [
        'version',
        'creator',
        'created_at',
        'updated_at',
    ]
    __memory__ = dict()

    def __init__(self, *arg, **kwargs) -> None:
        self.__dict__ = self._create_empty()
        self.__dict__.update({
            self.__data__: dict(*arg, **kwargs),
        })

    def _create_empty(self) -> dict:
        now = datetime.now().isoformat()
        return {
            'version': __version__,
            'creator': package_name,
            'created_at': now,
            'updated_at': now,
            self.__data__: dict(),
        }

    def __getitem__(self, key: Union[str, List[str]]) -> Union[Any, List[Any]]:
        return self.get(key)

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

    @decorater.copy_doc(stringify)
    def __repr__(self) -> str:
        return stringify(list(self.data.values()))

    @decorater.copy_doc(stringify)
    def __str__(self) -> str:
        return str(self.__repr__())

    def __len__(self) -> int:
        return len(self.data)

    def keys(self) -> list:
        return self.data.keys()

    def items(self) -> list:
        return self.data.items()

    def values(self) -> list:
        return self.data.values()

    @property
    def version(self) -> str:
        return self.__dict__.get('version')

    @property
    def data(self) -> dict:
        return self.__dict__.get(self.__data__)

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
        """Get objects by given IDs when list is given.
        When single string is given, returns single object by given key

        Args:
            key (str | List[str]): single key or list-like
            default (Any, optional): default value if not exists. Defaults to None.

        Returns:
            Any | List[Any]: single object or list-like

        Examples:
            >>> db.get('kcbPuqpfV3YSHT8YbECjvh')
            {...}
            >>> db.get(['kcbPuqpfV3YSHT8YbECjvh'])
            [{...}]
            >>> db.get(['kcbPuqpfV3YSHT8YbECjvh', 'jmJKBJBAmGESC3rGbSb62T'])
            [{...}, {...}]
        """
        _type, _keys = from_maybe_list(key)
        values = [self.data.get(k, default) for k in _keys]
        return return_maybe(_type, values)

    def update(self, mapping: Union[dict, tuple] = (), **kwargs) -> None:
        """Note that this method overrides database itself.
        """
        self._update_timestamp()
        self.data.update(mapping, **kwargs)

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
        type_id, ids = from_maybe_list(id)
        type_value, values = from_maybe_list(value)
        if len(ids) != len(values):
            raise ValueError(
                'Can not match ids and values. please check type and length of them')
        for index in range(len(ids)):
            _id, _value = ids[index], values[index]
            target = dict()
            target[_id] = _value
            self.data.update(target)
        self._update_timestamp()
        return return_maybe(type_id, values)

    def add(self, item: Union[Any, List[Any]]) -> Union[str, List[str]]:
        """
        Args:
            item (Union[Any, List[Any]]): Object(s) to add to database

        Returns:
            Union[str, List[str]]: Automatically generated ID of added item
        """
        _type, _items = from_maybe_list(item)

        ids = []
        for i in _items:
            uid = shortuuid.uuid()
            self.data[uid] = i
            ids.append(uid)

        self._update_timestamp()
        return return_maybe(_type, ids)

    def remove(self, key: Union[str, List[str]]) -> Union[Any, List[Any]]:
        """
        Args:
            key (Union[str, List[str]]): ID(s) to remove from database

        Returns:
            Union[Any, List[Any]]: removed items
        """
        _type, _keys = from_maybe_list(key)
        popped = [self.data.pop(key) for key in _keys]
        self._update_timestamp()
        return return_maybe(_type, popped)

    def all(self) -> List[Any]:
        """Provide all items in database.

        Returns:
            List[Any]: All items as list
        """
        return list(self.data.values())

    def clear(self) -> None:
        """Clear all items. This method updates timestamp in metadata.
        """
        self.data.clear()
        self._update_timestamp()

    def find(self, func: Callable[..., bool]) -> List[str]:
        """Returns array of IDs that satisfies the provided testing function.

        Args:
            func (Callable[..., bool]):
                A function to execute for each items in database.
                It will call `func(value)` to determine boolean.

        Returns:
            List[str]: array with id of found items
        """
        ids = []
        for object_id, value in self.data.items():
            found = func(value)
            if found:
                ids.append(object_id)
        return ids

    def has(self, key: Union[str, List[str]]) -> Union[bool, List[bool]]:
        """performs to determine whether has key

        Args:
            key (Union[str, List[str]]): to find with string(s) as key

        Returns:
            Union[bool, List[bool]]: boolean or array of boolean.
        """
        _type, _keys = from_maybe_list(key)
        key_set = set(self.data.keys())
        values = [k in key_set for k in _keys]
        return return_maybe(_type, values)

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
        """Save its states and all items at that time.
        """
        self.__memory__ = copy.deepcopy(self.__dict__)

    def rollback(self) -> None:
        """Restore all states and items from latest commit.
        """
        self.__dict__ = copy.deepcopy(self.__memory__)

    def load(
        self,
        path: str,
        file_args: dict = dict(
            mode="r",
            encoding="utf-8",
        ),
        json_args: dict = dict()
    ) -> 'Database':
        """Load database object from a file

        Args:
            path (str): a string containing a file name to load.
            file_args (dict, optional):
                keyword arguments for file `open(**kwagrs)`.
                Defaults to dict( mode="r", encoding="utf-8", ).
            json_args (dict, optional):
                keyword arguments for `json.loads(**kwargs)`.
                Defaults to dict().

        Raises:
            AttributeError:
                when JSON file does not contain keys and values
                to read into valid Database object.

        Returns:
            Database: itself
        """
        path = os.path.abspath(path)
        file_args = override_dict(file_args, dict(
            mode="r",
            encoding="utf-8",
        ))
        json_args = override_dict(json_args, dict())

        with open(path, **file_args) as f:
            raw = json.loads(f.read(), **json_args)

        self._create(raw)
        return self

    def _create(self, raw: Union[dict, list]) -> None:
        self.__dict__ = self._create_empty()

        if type(raw) == dict:
            keys_in_raw = set(raw.keys())
            field_keys = set(self.__metadata__ + [self.__data__])
            is_fields_valid = len(field_keys - keys_in_raw) == 0
            if is_fields_valid:
                self.__dict__.update({
                    'version': raw['version'],
                    'creator': raw['creator'],
                    'created_at': raw['created_at'],
                    'updated_at': raw['updated_at'],
                    self.__data__: raw[self.__data__],
                })
            else:
                self.add(raw)
        elif type(raw) == list:
            self.add(raw)

    def save(
        self,
        path: str,
        file_args: dict = dict(
            mode="w",
            encoding="utf-8",
        ),
        json_args: dict = dict(
            sort_keys=True,
        ),
        make_dirs: bool = False,
    ) -> None:
        """Save database object into a file as JSON format

        Args:
            path (str): a string containing a file name to save.
            file_args (dict, optional):
                keyword arguments for file `open(**kwagrs)`.
                Defaults to dict( mode="w+", encoding="utf-8", ).
            json_args (dict, optional):
                keyword arguments for `json.dumps(**kwargs)`.
                Defaults to dict( sort_keys=True, ).
            make_dirs (bool, optional):
                create non-exists directories in given path.
                Defaults to False.
        """
        path = os.path.abspath(path)
        file_args = override_dict(file_args, dict(
            mode="w+",
            encoding="utf-8",
        ))
        json_args = override_dict(json_args, dict(
            sort_keys=True,
        ))

        if make_dirs:
            dirname = os.path.dirname(path)
            if not os.path.exists(dirname):
                os.makedirs(dirname, exist_ok=True)

        with open(path, **file_args) as f:
            dict_out = self.__exports_only_publics()
            f.write(json.dumps(dict_out, **json_args))
