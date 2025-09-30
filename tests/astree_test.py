from astree import AstNode
from tokens import string_to_tokens, shunting_yard
import pytest


# TODO: Collect a (string, tokens, AST) triple dataset.


@pytest.fixture
def tokens_rpn():
    return shunting_yard(string_to_tokens("1 + exp y oq2"))


@pytest.fixture
def tokens_infix():
    return string_to_tokens("1 + exp y oq2")


def test_astify_rpn():
    pass


def test_astify_expr():
    pass


@pytest.mark.parametrize("string", ["1 + exp y oq2"])
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
