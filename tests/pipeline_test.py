import pytest

from astree import AstNode
from pipeline import (
    differentiation_group,
    differentiation_pipeline,
    normalisation_group,
)

"""
        normalisation_rules[0],
        Flattening(),
        CanonicalOrdering(),
        Evaluation(),
        Simplification(),
"""

@pytest.fixture
def test_expr():
    return AstNode.astify("(3 + ((x - 2) + 5)) * (1 * -4)")

def test_normalisation_group(test_expr: AstNode):
    normalisation_group.apply_all(test_expr)
    expected_expr = AstNode.astify("-4 * (6 + x)")
    assert test_expr.is_equal(expected_expr)

