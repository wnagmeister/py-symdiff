from tokens import Variable, Token
from astree import AstNode
import pytest
from tests.tokens_test import test_expressions_full

# pyright: reportUnusedVariable=false

rpn_tokens_asttree = [(rpn, ast) for (infix, rpn, ast, var) in test_expressions_full]
asttree = [ast for (infix, rpn, ast, var) in test_expressions_full]
asttree_varis = [(ast, varis) for (infix, rpn, ast, varis) in test_expressions_full]


@pytest.mark.parametrize("rpn_tokens, asttree", rpn_tokens_asttree)
def test_astify_rpn(rpn_tokens: list[Token], asttree: AstNode):
    assert AstNode.astify_rpn(rpn_tokens).is_equal(asttree)


# @pytest.mark.parametrize("asttree", asttree)
def test_overload_add():
    pass


def test_overload_mul():
    pass


def test_overload_sub():
    pass


def test_overload_pow():
    # Implement when ^ is properly implemented as a Operator object
    pass


@pytest.mark.parametrize("asttree", asttree)
def test_copy(asttree: AstNode):
    asttree_copy = asttree.copy()
    assert not asttree_copy == asttree
    assert asttree_copy.is_equal(asttree)
    for node_copy, node in zip(asttree_copy, asttree):
        match node.value:
            case float():
                assert node_copy.value == node.value
            case Variable():
                assert node_copy.value == node.value
                assert node_copy.value is not node.value
            case _:
                assert node_copy.value == node.value
                assert node_copy.value is node.value


@pytest.mark.parametrize("asttree, varis", asttree_varis)
def test_variables(asttree: AstNode, varis: set[Variable]):
    assert asttree.variables() == varis
