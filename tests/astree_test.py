from tokens import Variable
from astree import AstNode
import pytest
from tests.tokens_test import string_expressions


@pytest.mark.parametrize("infix_string, rpn_tokens, asttree", string_expressions)
def test_astify_rpn(infix_string, rpn_tokens, asttree):
    assert AstNode.astify_rpn(rpn_tokens).is_equal(asttree)


@pytest.fixture(params=string_expressions)
def test_asttree(request):
    return request.param[2]


def test_overload_add(test_asttree):
    pass


def test_overload_mul():
    pass


def test_overload_sub():
    pass


def test_overload_pow():
    # Implement when ^ is properly implemented as a Operator object
    pass


def test_copy(test_asttree):
    test_asttree_copy = test_asttree.copy()
    assert not test_asttree_copy == test_asttree
    assert test_asttree_copy.is_equal(test_asttree)
    for node_copy, node in zip(test_asttree_copy, test_asttree):
        match node.value:
            case float():
                assert node_copy.value == node.value
            case Variable():
                assert node_copy.value == node.value
                assert node_copy.value is not node.value
            case _:
                assert node_copy.value == node.value
                assert node_copy.value is node.value
