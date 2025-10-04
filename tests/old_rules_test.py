from symbols import Variable
from astree import AstNode
from old_rules import (
    flatten_recursive,
    sort_commutative,
    additive_identity,
    multiplicative_identity,
    multiplication_zero,
)


def test_flatten_recursive():
    expr = AstNode.astify("y * ( ( 2 + x ) + -4 )")
    assert flatten_recursive(expr)
    assert expr.children[1].children[0].value == 2
    assert expr.children[1].children[1].value == Variable("x")
    assert expr.children[1].children[2].value == -4


def test_sort_commutative():
    expr = AstNode.astify("x + 3 + -5.7 + exp ( 11 ) + y")
    flatten_recursive(expr)
    sort_commutative(expr)
    assert [repr(child.value) for child in expr.children] == [
        "-5.7",
        "3.0",
        "x",
        "y",
        "exp",
    ]


def test_additive_identity():
    expr = AstNode.astify("( x + 0 ) + ( 0 + 9 )")
    assert additive_identity(expr)
    assert expr.children[0].value == Variable("x")
    assert expr.children[1].value == 9
    expr = AstNode.astify("y - 0")
    assert not additive_identity(expr)


def test_multiplicative_identity():
    expr = AstNode.astify("( x * 1 ) * ( 1 * 9 )")
    assert multiplicative_identity(expr)
    assert expr.children[0].value == Variable("x")
    assert expr.children[1].value == 9
    expr = AstNode.astify("y + 1")
    assert not multiplicative_identity(expr)


def test_multiplication_zero():
    expr = AstNode.astify("( x * 0 ) + ( 0 * 9 )")
    assert multiplication_zero(expr)
    assert expr.children[0].value == 0
    assert expr.children[1].value == 0
    expr = AstNode.astify("y + 0")
    assert not multiplication_zero(expr)
