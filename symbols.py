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
    def __init__(self, string: str, arity: int, func):
        self.string = string
        self.arity = arity
        self.func = func

    def is_op(self, string):
        return self.string == string

    def __eq__(self, other) -> bool:  # TODO: Use this not above
        if isinstance(other, Operator):
            return self.string == other.string
        else:
            return False

    def __repr__(self):
        return self.string


"""Dictionary of operators, ordered from lowest precedence to highest."""
operators = {
    "+": Operator("+", 2, lambda x, y: x + y),
    "-": Operator("-", 2, lambda x, y: x - y),
    "*": Operator("*", 2, lambda x, y: x * y),
    "/": Operator("/", 2, lambda x, y: x / y),
    "sq": Operator("sq", 1, lambda x: x * x),
    "exp": Operator("exp", 1, math.exp),
    "sin": Operator("sin", 1, math.sin),
    "cos": Operator("cos", 1, math.cos),
    "ln": Operator("ln", 1, math.log),
    "D": Operator("D", 2, None),
}

if __name__ == "__main__":
    pass
