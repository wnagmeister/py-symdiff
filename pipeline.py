from astree import AstNode
from rules import (
    Transformation,
    Flattening,
    CanonicalOrdering,
    Evaluation,
    Simplification,
)
from match import normalisation_rules, differentiation_rules
from typing import Sequence


class TransformationPipeline:
    def __init__(self, transformations: Sequence[Transformation]):
        self.transformations = transformations

    def apply_root(self, expr: AstNode):
        while True:
            changed: bool = False
            for transformation in self.transformations:
                changed = transformation.apply_root(expr) or changed
            if not changed:
                break

    def apply(self, expr: AstNode):
        for sub_expr in expr:
            self.apply_root(sub_expr)

    def apply2(self, expr: AstNode):
        while True:
            changed: bool = False
            for transformation in self.transformations:
                changed = transformation.apply_all(expr) or changed
            if not changed:
                break


normalisation = TransformationPipeline(
    [
        normalisation_rules[0],
        Flattening(),
        CanonicalOrdering(),
        Evaluation(),
        Simplification(),
    ]
)


differentiation = TransformationPipeline(differentiation_rules)
