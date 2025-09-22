def isnum(token):
    return token.isnumeric()


def isop(token):
    return token in "+-*/"


def isfunc(token):
    return token == "sin"


def pre(op) -> int:
    if isfunc(op):
        return 4
    if op in "*/":
        return 3
    if op in "+-":
        return 2
    return 0


def shunting_yard(tokens: list[str]):
    outs = []  # mypy: ignore
    ops = []  # mypy: ignore
    for token in tokens:
        if isnum(token):
            outs.append(token)

        elif isfunc(token):
            ops.append(token)

        elif isop(token):

            while len(ops) > 0 and ops[-1] != "(" and pre(ops[-1]) >= pre(token):
                outs.append(ops.pop())
            ops.append(token)

        elif token == "(":
            ops.append(token)

        elif token == ")":
            assert len(ops) > 0
            while ops[-1] != "(":
                outs.append(ops.pop())
            assert ops[-1] == "("
            ops.pop()
            if len(ops) > 0 and isfunc(ops[-1]):
                outs.append(ops.pop())

    for token in ops:
        assert ops[-1] != "("
        outs.append(ops.pop())

    return outs


def main():
    inf = "( 1 + 2 ) * ( 3 + 4 )"
    print(inf)
    tokens = inf.split()
    result = shunting_yard(tokens)
    print(" ".join(result))



main()
