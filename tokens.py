from symbols import Operator, Variable, operators

type Token = float | Operator | Variable
type Operand = float | Variable


def tokenify(string: str) -> Token:
    """Converts a string representing a number, variable or operator into a
    token. Strings not recognised as numbers or operators become variables.
    """
    try:
        return float(string)
    except ValueError:
        if operator := operators.get(string):
            return operator
        else:
            return Variable(string)


def space_around_string(string: str) -> str:
    for char in "()+*/":
        string = string.replace(char, f" {char} ")
    return string


def string_to_tokens(string: str) -> list[Token]:
    """Converts a string expression into a list of corresponding tokens."""
    string = space_around_string(string)
    str_tokens = string.split()
    tokens = [tokenify(str_token) for str_token in str_tokens]
    return tokens


def shunting_yard(tokens: list[Token]) -> list[Token]:
    """Shunting yard algorithm. Currently considers basic operators and single
    variable functions. Associativity is assumed to be always left, and
    differentiation w.r.t. x is implemented as the highest precedence infix
    operator, notated:
        x D y   <->    (d/dx)y

    """
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
                    and not operator_stack[-1] == operators["("]
                    and operator_stack[-1] >= token
                ):
                    out_stack.append(operator_stack.pop())
                operator_stack.append(token)

            elif token == operators["("]:
                operator_stack.append(token)

            elif token == operators[")"]:
                assert len(operator_stack) > 0
                while not operator_stack[-1] == operators["("]:
                    out_stack.append(operator_stack.pop())
                assert operator_stack[-1] == operators["("]
                operator_stack.pop()

                if len(operator_stack) > 0 and operator_stack[-1].arity == 1:
                    out_stack.append(operator_stack.pop())

    while len(operator_stack) > 0:
        assert not operator_stack[-1] == operators["("]
        out_stack.append(operator_stack.pop())

    return out_stack


if __name__ == "__main__":
    pass
