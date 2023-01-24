from typing import Any, Union

from .operator import (
    Operator,
    compare,
    invert_operator
)


class Comparator:
    def __call__(self, item: dict) -> bool:
        return self.evaluate(item)

    def evaluate(self, other: dict) -> bool:
        pass


class Condition(Comparator):
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

    def copy(self) -> 'Condition':
        return Condition(key=self.key, value=self.value, operator=self.operator)

    def __invert__(self) -> 'Condition':
        copy = self.copy()
        copy.operator = invert_operator(self.operator)
        return copy

    def __and__(self, other: 'Condition') -> 'Conditions':
        return Conditions(lvalue=self, rvalue=other, operator=Operator.AND)

    def __rand__(self, other: 'Condition') -> 'Conditions':
        return Conditions(lvalue=other, rvalue=self, operator=Operator.AND)

    def __or__(self, other: 'Condition') -> 'Conditions':
        return Conditions(lvalue=self, rvalue=other, operator=Operator.OR)

    def __ror__(self, other: 'Condition') -> 'Conditions':
        return Conditions(lvalue=other, rvalue=self, operator=Operator.OR)

    def evaluate(self, item: dict) -> bool:
        key = str(self.key)
        if not key in item:
            return None
        return compare(item[key], self.value, self.operator)


class Conditions(Comparator):
    _left: Union[Condition, 'Conditions']
    _right: Union[Condition, 'Conditions']
    _oper: Operator

    def __init__(
        self,
        lvalue: Union[Condition, 'Conditions'],
        rvalue: Union[Condition, 'Conditions'],
        operator: Operator
    ) -> None:
        self._left = lvalue
        self._right = rvalue
        self._oper = operator

    def evaluate(self, other: dict) -> bool:
        l, r, op = self._left, self._right, self._oper
        return compare(l(other), r(other), op)

    def copy(self) -> 'Conditions':
        return Conditions(
            lvalue=self._left,
            rvalue=self._right,
            operator=self._oper,
        )

    def __invert__(self) -> 'Conditions':
        """This is for NOT operation.
        For example, when you call `~(a & b)` it means `not (a and b)`.
        """
        inst = self.copy()
        inst._oper = invert_operator(inst._oper)
        return inst

    def invert(self) -> 'Conditions':
        """According boolean algebra that satisfies De Morgan's laws
        In case of `(a & b).invert()`, it returns having the meaning of
        `(not a) or (not b)` that is equivalent to `(a and b)` in logical.
        """
        return Conditions(
            lvalue=~self._left,
            rvalue=~self._right,
            operator=invert_operator(self._oper),
        )

    def __and__(self, other: Union[Condition, 'Conditions']) -> 'Conditions':
        return Conditions(lvalue=self, rvalue=other, operator=Operator.AND)

    def __rand__(self, other: Union[Condition, 'Conditions']) -> 'Conditions':
        return Conditions(lvalue=other, rvalue=self, operator=Operator.AND)

    def __or__(self, other: Union[Condition, 'Conditions']) -> 'Conditions':
        return Conditions(lvalue=self, rvalue=other, operator=Operator.OR)

    def __ror__(self, other: Union[Condition, 'Conditions']) -> 'Conditions':
        return Conditions(lvalue=other, rvalue=self, operator=Operator.OR)

    def __repr__(self) -> str:
        res = [self._left, self._oper, self._right]
        return "({})".format(', '.join(list(map(repr, res))))


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
