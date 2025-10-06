from symbols import Variable
from astree import AstNode
from rules import Flattening, CanonicalOrdering, Evaluation, Simplification
import pytest
import math


@pytest.fixture
def flattener():
    flatterner = Flattening()
    return flatterner


@pytest.fixture
def canonical_orderer():
    canonical_orderer = CanonicalOrdering()
    return canonical_orderer


@pytest.fixture
def evaluator():
    evaluator = Evaluation()
    return evaluator


@pytest.fixture
def simplifier():
    simplifier = Simplification()
    return simplifier


def test_flattening(flattener: Flattening):
    expr = AstNode.astify("y * ((2 + x) + -4)")
    assert flattener.apply_all(expr)
    assert expr.children[1].children[0].value == 2
    assert expr.children[1].children[1].value == Variable("x")
    assert expr.children[1].children[2].value == -4


def test_canonicalordering(flattener: Flattening, canonical_orderer: CanonicalOrdering):
    expr = AstNode.astify("x + 3 + -5.7 + exp(11) + y")
    assert flattener.apply_all(expr)
    assert canonical_orderer.apply_all(expr)
    assert [repr(child.value) for child in expr.children] == [
        "-5.7",
        "3.0",
        "x",
        "y",
        "exp",
    ]


def test_evaluation(evaluator: Evaluation):
    # expr = AstNode.astify("1 + 2")
    # assert evaluator.apply_all(expr)
    # assert expr.value == 3
    # expr = AstNode.astify("exp(2) * (4 + 1)")
    # assert evaluator.apply_all(expr)
    # assert expr.value == 5 * math.exp(2)
    # expr = AstNode.astify("5 * (4 + 1) + exp (x)")
    # assert evaluator.apply_all(expr)
    # expected_expr = AstNode.astify("25 + exp (x)")
    # assert expr.is_equal(expected_expr)
    pass


def test_simplification(simplifier: Simplification):
    expr = AstNode.astify("(x + 0) - (1 * 7)")
    assert simplifier.apply_all(expr)
    expected_expr = AstNode.astify("x - 7")
    assert expr.is_equal(expected_expr)
    expr = AstNode.astify("((0 + 0) + 0 + ln(y)) / (y * 0)")
    assert simplifier.apply_all(expr)
    expected_expr = AstNode.astify("ln(y) / 0")
    assert expr.is_equal(expected_expr)
