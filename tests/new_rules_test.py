from symbols import Variable
from astree import AstNode
from new_rules import Flattening, CanonicalOrdering, Evaluation
import pytest


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


def test_flattening(flattener):
    expr = AstNode.astify("y * ( ( 2 + x ) + -4 )")
    assert flattener.apply_all(expr)
    assert expr.children[1].children[0].value == 2
    assert expr.children[1].children[1].value == Variable("x")
    assert expr.children[1].children[2].value == -4


def test_canonicalordering(flattener, canonical_orderer):
    expr = AstNode.astify("x + 3 + -5.7 + exp ( 11 ) + y")
    assert flattener.apply_all(expr)
    assert canonical_orderer.apply_all(expr)
    assert [repr(child.value) for child in expr.children] == [
        "-5.7",
        "3.0",
        "x",
        "y",
        "exp",
    ]


scalar_expressions = []


def test_evaluation(evaluator):
    expr = AstNode.astify("1 + 2")
    assert evaluator.apply_all(expr)
    assert expr.value == 3
    expr = AstNode.astify("5 * ( 4 - 1 )")
    assert evaluator.apply_all(expr)
    assert expr.value == 15
