import math
from typing import Any, Callable, Self


class Symbol:
    def __init__(self, string: str):
        self.string = string

    def __eq__(self, other: Any):
        if type(self) is type(other):
            return self.string == other.string
        else:
            return False

    def __repr__(self):
        return self.string


class Variable(Symbol):
    def __hash__(self):
        return hash(self.string)

class Operator(Symbol):
    def __init__(
        self,
        string: str,
        arity: int,
        precedence: int,
        associative: str,
        commutative: bool,
    ):
        super().__init__(string)
        self.arity = arity
        self.precedence = precedence
        self.associative = associative
        self.commutative = commutative

    def __ge__(self, other: Self):
        return self.precedence >= other.precedence


class UnaryOperator(Operator):
    def __init__(
        self,
        string: str,
        arity: int,
        precedence: int,
        associative: str,
        commutative: bool,
        func: Callable[[float], float],
    ):
        super().__init__(string, arity, precedence, associative, commutative)
        self.arity = 1
        self.func = func


class BinaryOperator(Operator):
    def __init__(
        self,
        string: str,
        arity: int,
        precedence: int,
        associative: str,
        commutative: bool,
        func: Callable[[float, float], float],
    ):
        super().__init__(string, arity, precedence, associative, commutative)
        self.arity = 2
        self.func = func


operators: dict[str, Operator] = {
    "+": BinaryOperator("+", 2, 1, "full", True, lambda x, y: x + y),
    "-": BinaryOperator("-", 2, 1, "left", False, lambda x, y: x - y),
    "*": BinaryOperator("*", 2, 2, "full", True, lambda x, y: x * y),
    "/": BinaryOperator("/", 2, 2, "left", False, lambda x, y: x / y),
    "^": BinaryOperator("^", 2, 3, "right", False, lambda x, y: x ** y),
    "sq": UnaryOperator("sq", 1, 4, "right", False, lambda x: x * x),
    "exp": UnaryOperator("exp", 1, 4, "right", False, math.exp),
    "sin": UnaryOperator("sin", 1, 4, "right", False, math.sin),
    "cos": UnaryOperator("cos", 1, 4, "right", False, math.cos),
    "ln": UnaryOperator("ln", 1, 4, "right", False, math.log),
    "D": Operator("D", 2, 5, "left", False),
    "(": Operator("(", 0, 0, "", False),
    ")": Operator(")", 0, 0, "", False),
}

if __name__ == "__main__":
    pass
