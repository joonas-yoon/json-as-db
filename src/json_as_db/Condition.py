from enum import Enum
from typing import Any, List, Callable, Union


class Operator(Enum):
    LESS_THAN = '<'
    LESS_EQUAL = '<='
    EQUAL = '=='
    NOT_EQUAL = '!='
    GREATER_THAN = '>'
    GREATER_EQUAL = '>='
    AND = '&'
    OR = '|'


def _compare(a: Any, b: Any, op: Operator):
    if a == None or b == None:
        return False
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
    elif op is Operator.AND:
        return a & b
    elif op is Operator.OR:
        return a | b
    else:
        raise NotImplementedError()


def _invert_operator(op: Operator):
    if op is Operator.LESS_THAN:       # <
        return Operator.GREATER_EQUAL  # ~(<) is (>=)
    elif op is Operator.LESS_EQUAL:    # <=
        return Operator.GREATER_THAN   # ~(<=) is (>)
    elif op is Operator.EQUAL:         # ==
        return Operator.NOT_EQUAL      # ~(==) is (!=)
    elif op is Operator.NOT_EQUAL:     # !=
        return Operator.EQUAL          # ~(!=) is (==)
    elif op is Operator.GREATER_THAN:  # >
        return Operator.LESS_EQUAL     # ~(>) is (<=)
    elif op is Operator.GREATER_EQUAL: # >=
        return Operator.LESS_THAN      # ~(>=) is (<)
    elif op is Operator.AND:           # and
        return Operator.OR             # ~(and) is (or)
    elif op is Operator.OR:            # or
        return Operator.AND            # ~(or) is (and)
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

    def __call__(self, item: dict) -> bool:
        return self._evaluate_by_key(item)

    def copy(self) -> 'Condition':
        return Condition(key=self.key, value=self.value, operator=self.operator)

    def __invert__(self) -> 'Condition':
        copy = self.copy()
        copy.operator = _invert_operator(self.operator)
        return copy

    def __and__(self, other: 'Condition') -> 'Conditions':
        return Conditions(lvalue=self, rvalue=other, operator=Operator.AND)

    def __rand__(self, other: 'Condition') -> 'Conditions':
        return Conditions(lvalue=other, rvalue=self, operator=Operator.AND)

    def __or__(self, other: 'Condition') -> 'Conditions':
        return Conditions(lvalue=self, rvalue=other, operator=Operator.OR)

    def __ror__(self, other: 'Condition') -> 'Conditions':
        return Conditions(lvalue=other, rvalue=self, operator=Operator.OR)

    def _evaluate_by_key(self, item: dict) -> bool:
        key = str(self.key)
        if not key in item:
            return None
        return self.evaluate(item[key])

    def evaluate(self, other: Any) -> bool:
        return _compare(other, self.value, self.operator)


class Conditions:
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
        return _compare(l(other), r(other), op)

    def __call__(self, item: dict) -> bool:
        return self.evaluate(item)

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
        inst._oper = _invert_operator(inst._oper)
        return inst

    def invert(self) -> 'Conditions':
        """According boolean algebra that satisfies De Morgan's laws
        In case of `(a & b).invert()`, it returns having the meaning of
        `(not a) or (not b)` that is equivalent to `(a and b)` in logical.
        """
        return Conditions(
            lvalue=~self._left,
            rvalue=~self._right,
            operator=_invert_operator(self._oper),
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
