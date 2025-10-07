from astree import AstNode
from pipeline import normalisation_group, differentiation_pipeline


def test_norm_mult():
    expr = AstNode.astify("x D (x * x)")
    normalisation_group.apply_all(expr)

def test_diff_mult():
    expr = AstNode.astify("x D (x * x)")
    differentiation_pipeline.apply_all(expr)


# def test_diff_add():
#     expr = AstNode.astify("x D (x + x)")
#     breakpoint()
#     differentiation_pipeline.apply_all(expr)
#     breakpoint()
