from astree import AstNode

h = 0.0001


def derivative_at(func, x0):
    return (func(x0 + h) - func(x0 - h)) / (2 * h)


def test():
    expr = "x sq 3 x * + 5 -"  # x^2 + 3x - 5
    dexpr = "2 x * 3 +"  # 2x + 3
    ast = AstNode.astify(expr)
    dast1 = ast.derivative()
    dast2 = AstNode.astify(dexpr)

    disreps = 0

    for i in range(-100, 100):
        d1 = dast1.evaluate(i / 10)
        d2 = dast2.evaluate(i / 10)
        print(d1 - d2)
        if d1 - d2 != 0.0:
            disreps += 1

    print(disreps)


def test2():
    X = AstNode.astify_const("x")
    Y = AstNode.astify_const("y")
    c2 = AstNode.astify_const(2)
    c5 = AstNode.astify_const(5)
    n7 = AstNode.astify_const(-7)
    c0 = AstNode.astify_const(0)

    ast = c5 / X - n7 * X * Y
    dast = ast.derivative()
    print(ast)
    print(
        "-----------------------------------------------------------------------------------------"
    )
    print(dast)

test()
test2()
