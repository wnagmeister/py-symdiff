from astree import AstNode
from match import PatternVariable, PatternMatching, Differentiation, normalisation_rules, differentiation_rules
import pytest

@pytest.fixture
def patternvariable_init_test():
	x = PatternVariable("x")
	assert a.match_type == "all"
	s = PatternVariable("s")
	assert s.match_type == float
	a = PatternVariable("a", float)
	assert a.match_type == float
	return x, s

patternvariables = patternvariable_init_test

@pytest.fixture
def test_exprs():
	expr1 = AstNode.astify("4 + exp ( x - s )")
	expr2 = AstNode.astify("-18")

def patternvariable_match_test(patternvariables, test_exprs):
	for patvar, expr in zip(patternvariables, test_exprs):
		assert patvar.match(expr)
	expr1, expr2 = test_exprs
	vars1 = expr1.vars()
	for var in vars1:
		assert not isinstance(var, PatternVariable)
	PatternVariable.patternify(expr1)
	patvars1 = expr1.vars()
	for patvar in patvars1:
		assert isinstance(patvar, PatternVariable)
	for var, patvar in zip(vars1, patvars1):
		assert repr(var) == repr(patvar)
	
def sub_to_add_test():
	pattern: AstNode = normalisation_rules[0].pattern
	expr: AstNode = AstNode.astify("x - 2")
	bindings: dict[PatternVariable, AstNode] = {}
	assert PatternMatching.match(expr, pattern, bindings)
	assert bindings[PatternVariable("f")].value == Variable("x")
	assert bindings[PatternVariable("g")].value == 2
	assert normalisation_rules[0].apply_all(expr)
	expected_expr = AstNode.astify("x + ( -1 * 2 )")
	assert expr.is_equal(expected_expr)