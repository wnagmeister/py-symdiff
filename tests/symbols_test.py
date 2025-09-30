from symbols import Variable, Operator, operators


def test_variable():
    x1 = Variable("xVar")
    x2 = Variable("xVar")
    assert x1 is not x2
    assert x1 == x2
    assert repr(x1) == "xVar"


def test_operators_dict():
    for i, key in enumerate(operators):
        if i == 0:
            prev_operator = operators[key]
        elif key not in "()sum":
            assert operators[key] >= prev_operator
            prev_operator = operators[key]
    assert operators["+"] >= operators["-"]
    assert operators["-"] >= operators["+"]
