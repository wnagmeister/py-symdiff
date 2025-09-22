from symbols import Variable, Operand, Operator, operators

operators["("] = Operator("(", 0, None, None)
operators[")"] = Operator(")", 0, None, None)


operator_precedence = [
    operators.get("/"),
    operators.get("*"),
    operators.get("-"),
    operators.get("+"),
]

lst = [9, 8, 7]


def precedence_ge(op1, op2):
    return operator_precedence.index(op1) >= operator_precedence.index(op2)


Operator.__ge__ = precedence_ge  # mypy: ignore


def tokenify(string: str) -> Operand | Operator:
    if string.lstrip("-").isnumeric():
        return Operand(float(string))
    elif operator := operators.get(string):
        return operator
    else:
        return Operand(Variable(string))


def string_to_tokens(string: str) -> list[Operand | Operator]:
    str_tokens = string.split()
    tokens = [tokenify(str_token) for str_token in str_tokens]
    return tokens


def shunting_yard(tokens: list[Operand | Operator]) -> list[Operand | Operator]:
    """shunting yard alg, to be implemented"""
    out_stack: list[Operand | Operator] = []
    operator_stack: list[Operator] = []

    for token in tokens:

        if isinstance(token, Operand):
            out_stack.append(token)

        elif isinstance(token, Operator):

            if token.arity == 1:
                operator_stack.append(token)

            elif token.arity == 2:
                while (
                    len(operator_stack) > 0
                    and not operator_stack[-1].is_op("(")
                    and operator_stack[-1] >= token
                ):
                    out_stack.append(operator_stack.pop())
                operator_stack.append(token)

            elif token.is_op("("):
                operator_stack.append(token)

            elif token.is_op(")"):
                assert len(operator_stack) > 0
                while not operator_stack[-1].is_op("("):
                    out_stack.append(operator_stack.pop())
                assert operator_stack[-1].is_op("(")
                operator_stack.pop()

                if len(operator_stack) > 0 and operator_stack[-1].arity == 1:
                    out_stack.append(operator_stack.pop())

    while len(operator_stack) > 0:
        assert not operator_stack[-1].is_op("(")
        out_stack.append(operator_stack.pop())

    return out_stack


if __name__ == "__main__":
    pass
