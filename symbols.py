import math

class Variable:
    def __init__(self, string):
        self.string = string

    def __eq__(self, other_var):
        return self.string == other_var.string

    def evaluate(self, x):
        return x

    def __repr__(self):
        return self.string


class Operator:
    def __init__(self, string: str, arity: int, func, diff):
        self.string = string
        self.arity = arity
        self.func = func
        self.diff = diff

    def is_op(self, string):
        return self.string == string

    def __eq__(self, other_op): # TODO: Use this not above
        return self.string == other_op.string 

    def __repr__(self):
        return self.string


operators = {
    "+": Operator("+", 2, lambda x, y: x + y, "##0 ##1 +"),
    "-": Operator("-", 2, lambda x, y: x - y, "##0 ##1 -"),
    "*": Operator("*", 2, lambda x, y: x * y, "##0 #1 * #0 ##1 * +"),
    "/": Operator("/", 2, lambda x, y: x / y, "##0 #1 * #0 ##1 * - #1 sq /"),
    "sq": Operator("sq", 1, lambda x: x * x, "2 #0 * ##0 *"),
    "exp": Operator("exp", 1, math.exp, "##0 #0 exp *"),
    "sin": Operator("sin", 1, math.sin, "##0 #0 cos *"),
    "cos": Operator("cos", 1, math.cos, "##0 #0 sin * -1 *"),
    "ln": Operator("ln", 1, math.log, "##0 #0 /"),
}

if __name__ == "__main__":
    pass
