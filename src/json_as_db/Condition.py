from enum import Enum
from typing import Any


class Operator(Enum):
    LESS_THAN = '<'
    LESS_EQUAL = '<='
    EQUAL = '=='
    NOT_EQUAL = '!='
    GREATER_THAN = '>'
    GREATER_EQUAL = '>='


def _compare(a: Any, b: Any, op: Operator):
    if op is Operator.LESS_THAN:
        return a < b
    elif op is Operator.LESS_EQUAL:
        return a <= b
    elif op is Operator.EQUAL:
        return a == b
    elif op is Operator.NOT_EQUAL:
        return a != b
    elif op is Operator.GREATER_THAN:
        return a > b
    elif op is Operator.GREATER_EQUAL:
        return a >= b
    else:
        raise NotImplementedError()


class Condition:
    key: str
    value: Any
    operator: Operator

    def __init__(self, key: str, value: Any, operator: Operator) -> None:
        self.key = key
        self.value = value
        self.operator = operator

    def __repr__(self) -> str:
        s = [
            f"key='{self.key}'",
            f"operator={self.operator}",
            f"value={repr(self.value)}",
        ]
        return f"Condition({', '.join(s)})"

    def __call__(self, obj_id: str, item: dict) -> bool:
        key = str(self.key)
        if not key in item:
            return False
        return _compare(item[key], self.value, self.operator)


class Key(str):
    def __lt__(self, value: Any) -> Condition:
        return self.__generate_condition__(value, Operator.LESS_THAN)

    def __le__(self, value: Any) -> Condition:
        return self.__generate_condition__(value, Operator.LESS_EQUAL)

    def __eq__(self, value: Any) -> Condition:
        return self.__generate_condition__(value, Operator.EQUAL)

    def __ne__(self, value: Any) -> Condition:
        return self.__generate_condition__(value, Operator.NOT_EQUAL)

    def __gt__(self, value: Any) -> Condition:
        return self.__generate_condition__(value, Operator.GREATER_THAN)

    def __ge__(self, value: Any) -> Condition:
        return self.__generate_condition__(value, Operator.GREATER_EQUAL)

    def __generate_condition__(self, value: Any, operator: Operator):
        return Condition(key=self, value=value, operator=operator)
