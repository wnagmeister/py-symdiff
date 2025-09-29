import math


class Variable:
    def __init__(self, string):
        self.string = string

    def __eq__(self, other) -> bool:
        if isinstance(other, Variable):
            return self.string == other.string
        else:
            return False

    def evaluate(self, x):
        return x

    def __repr__(self):
        return self.string

    def __hash__(self):
        return hash(self.string)


class Operator:
    def __init__(
        self, string: str, arity: int, precedence: int, associativity: str, func
    ):
        self.string = string
        self.arity = arity
        self.precedence = precedence
        self.associativity = associativity
        self.func = func

    def __eq__(self, other) -> bool:
        if isinstance(other, Operator):
            return self.string == other.string
        else:
            return False

    def __ge__(self, other) -> bool:
        return self.precedence >= other.precedence

    def __repr__(self):
        return self.string


operators = {
    "+": Operator("+", 2, 1, "left", lambda x, y: x + y),
    "-": Operator("-", 2, 1, "left", lambda x, y: x - y),
    "*": Operator("*", 2, 2, "left", lambda x, y: x * y),
    "/": Operator("/", 2, 2, "left", lambda x, y: x / y),
    "sq": Operator("sq", 1, 3, "right", lambda x: x * x),
    "exp": Operator("exp", 1, 3, "right", math.exp),
    "sin": Operator("sin", 1, 3, "right", math.sin),
    "cos": Operator("cos", 1, 3, "right", math.cos),
    "ln": Operator("ln", 1, 3, "right", math.log),
    "D": Operator("D", 2, 4, "left", None),
}

if __name__ == "__main__":
    pass
