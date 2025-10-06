from astree import AstNode
from match import (
    PatternVariable,
    PatternMatching,
    normalisation_rules,
    differentiation_rules,
)
import pytest
from typing import Sequence


@pytest.fixture
def test_patternvariable_init():
    x = PatternVariable("x")
    assert x.match_type == "all"
    s = PatternVariable("s")
    assert s.match_type == float
    a = PatternVariable("a", float)
    assert a.match_type == float
    return x, s


patternvariables = test_patternvariable_init


@pytest.fixture
def test_exprs():
    expr1 = AstNode.astify("4 + exp(x - s)")
    expr2 = AstNode.astify("-18")
    return expr1, expr2


def test_patternvariable_match(
    patternvariables: Sequence[PatternVariable], test_exprs: Sequence[AstNode]
):
    for patvar, expr in zip(patternvariables, test_exprs):
        assert patvar.match(expr)
    expr1, expr2 = test_exprs
    vars1 = expr1.variables()
    for var in vars1:
        assert not isinstance(var, PatternVariable)
    PatternVariable.patternify(expr1)
    patvars1 = expr1.variables()
    for patvar in patvars1:
        assert isinstance(patvar, PatternVariable)
    for var, patvar in zip(vars1, patvars1):
        assert repr(var) == repr(patvar)


def test_sub_to_add():
    pattern: AstNode = normalisation_rules[0].pattern
    expr: AstNode = AstNode.astify("x - 2")
    bindings: dict[PatternVariable, AstNode] = {}
    assert PatternMatching.match(expr, pattern, bindings)
    assert bindings[PatternVariable("f")].value.string == "x"
    assert bindings[PatternVariable("g")].value == 2
    assert normalisation_rules[0].apply_all(expr)
    expected_expr = AstNode.astify("x + (-1 * 2)")
    assert expr.is_equal(expected_expr)


def test_differentiation():
    expr: AstNode = AstNode.astify("x D 2")
    assert differentiation_rules[0].apply_all(expr)
    assert expr.value == 0
    expr = AstNode.astify("x D (f + exp(g))")
    assert differentiation_rules[2].apply_all(expr)
    expr = AstNode.astify("x D (x * x)")
    assert differentiation_rules[3].apply_all(expr)
    assert differentiation_rules[1].apply_all(expr)
