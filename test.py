from astree import AstNode


def test1():
    expr = "x sq 3 x * + 5 -"  # x^2 + 3x - 5
    dexpr = "2 x * 3 +"  # 2x + 3
    ast = AstNode.astify(expr)
    dast1 = ast.derivative()
    dast2 = AstNode.astify(dexpr)

    h = 0.00001
    for i in range(-10, 10):
        a1 = ast.evaluate(i / 10)
        a2 = (i / 10) ** 2 + 3 * (i / 10) - 5
        assert a1 - a2 < h
    for i in range(-10, 10):
        d1 = dast1.evaluate(i / 10)
        d2 = dast2.evaluate(i / 10)
        assert d1 - d2 < h


def test2():
    X = AstNode.astify_const("x")
    Y = AstNode.astify_const("y")
    c2 = AstNode.astify_const(2)
    c5 = AstNode.astify_const(5)
    n7 = AstNode.astify_const(-7)
    c0 = AstNode.astify_const(0)

    ast = c5 / X - n7 * X * Y
    dast = ast.derivative()

    h = 0.00001
    for i in range(-10, 10):
        if i == 0:
            continue
        a1 = ast.evaluate(i / 10)
        x = i / 10
        a2 = 5 / x - (-7) * x * x
        assert a1 - a2 < h


def main():
    test1()
    test2()


if __name__ == "__main__":
    main()
