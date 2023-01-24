from enum import Enum
from typing import Any


class Operator(Enum):
    LESS_THAN = '<'
    LESS_EQUAL = '<='
    EQUAL = '=='
    NOT_EQUAL = '!='
    GREATER_THAN = '>'
    GREATER_EQUAL = '>='
    AND = '&'
    OR = '|'


def compare(a: Any, b: Any, op: Operator):
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
        if a != None and b != None:
            return a & b
        return False
    elif op is Operator.OR:
        if a != None and b != None:
            return a | b
        return False
    else:
        raise NotImplementedError()


def invert_operator(op: Operator):
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
