from astree import AstNode
from tokens import string_to_tokens, shunting_yard
import pytest


string_expressions = """3 * ( x + 2 ) - sin ( y )
a / ( b + cos ( c ) )
( x + y ) * ( 4 - cos ( z ) )
( 5 + sin ( x ) ) / ( 2 + y )
2 * ( sin ( x + y ) - 3 ) * z""".split(
    "\n"
)

"""
3*(x+2)-sin(y)
a/(b+cos(c))
(x+y)*(4-cos(z))
(5+sin(x))/(2+y)
2*(sin(x+y)-3)*z
"""


@pytest.fixture(params=string_expressions)
def tokens_infix(request):
    return string_to_tokens(request.param)


@pytest.fixture
def tokens_rpn(tokens_infix):
    return shunting_yard(tokens_infix)


def test_astify_rpn(tokens_rpn):
    expr = AstNode.astify_rpn(tokens_rpn)


def test_astify_expr():
    pass


@pytest.mark.parametrize("string", string_expressions)
def test_astify(string):
    expr = AstNode.astify(string)


def test_overload_add():
    pass


def test_overload_mul():
    pass


def test_overload_sub():
    pass


def test_overload_pow():
    # Implement when ^ is properly implemented as a Operator object
    pass


def test_copy():
    pass
