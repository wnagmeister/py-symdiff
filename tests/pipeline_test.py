from astree import AstNode
from pipeline import normalisation, differentiation

def test_diff_full():
	expr = AstNode.astify("x D (x * x)")
	breakpoint()
	differentiation.apply(expr)