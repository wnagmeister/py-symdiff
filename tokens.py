from symbols import Variable, Operator, operators

operators["("] = Operator("(", 0, 0, "", None)
operators[")"] = Operator(")", 0, 0, "", None)


def precedence_ge(op1, op2):
    for key in operators:
        if key == op1:
            return -1
        if key == op2:
            return 1


type Token = float | Operator | Variable
type Operand = float | Variable


def tokenify(string: str) -> Token:
    if string.lstrip("-").isnumeric():
        return float(string)
    elif operator := operators.get(string):
        return operator
    else:
        return Variable(string)


def string_to_tokens(string: str) -> list[Token]:
    str_tokens = string.split()
    tokens = [tokenify(str_token) for str_token in str_tokens]
    return tokens


def shunting_yard(tokens: list[Token]) -> list[Token]:
    """shunting yard alg, to be implemented"""
    out_stack: list[Token] = []
    operator_stack: list[Operator] = []

    for token in tokens:

        if isinstance(token, float | Variable):
            out_stack.append(token)

        elif isinstance(token, Operator):

            if token.arity == 1:
                operator_stack.append(token)

            elif token.arity == 2:
                while (
                    len(operator_stack) > 0
                    and not operator_stack[-1] == operators.get("(")
                    and operator_stack[-1] >= token
                ):
                    out_stack.append(operator_stack.pop())
                operator_stack.append(token)

            elif token == operators.get("("):
                operator_stack.append(token)

            elif token == operators.get(")"):
                assert len(operator_stack) > 0
                while not operator_stack[-1] == operators.get("("):
                    out_stack.append(operator_stack.pop())
                assert operator_stack[-1] == operators.get("(")
                operator_stack.pop()

                if len(operator_stack) > 0 and operator_stack[-1].arity == 1:
                    out_stack.append(operator_stack.pop())

    while len(operator_stack) > 0:
        assert not operator_stack[-1] == operators.get("(")
        out_stack.append(operator_stack.pop())

    return out_stack


if __name__ == "__main__":
    pass
