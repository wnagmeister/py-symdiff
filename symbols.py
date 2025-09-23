import math

class Variable:
    def __init__(self, string):
        self.string = string

    def equals(self, other_var):
        """checks if two variables are equal.
        would prefer if for each string there is only one variable, with
        several 'references' to it but alas we work this way
        """
        return self.string == other_var.string

    # def __eq__(self, other_var): # TODO: replace equals() with overloaded ==
    #     return self.string == other_var.string    This apparent doesnt work because it breaks the common variables set as unhashable

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


class Operand:  # TODO: Delete this class, use just classes Operator, Variable, Scalar,
    def __init__(self, opvalue: float | Variable):
        self.opvalue = opvalue

    def is_optype(self, class_type):
        return isinstance(self.opvalue, class_type)

    def __repr__(self):
        if self.is_optype(Variable):
            return self.opvalue.__repr__()
        return str(self.opvalue)

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

common_variables = {
    Variable("x"),
    Variable("y")
}

if __name__ == "__main__":
    pass
