from typing import Sequence

from astree import AstNode
from match import differentiation_rules, normalisation_patterns
from rules import (
    CanonicalOrdering,
    Evaluation,
    Flattening,
    UnFlattening,
    Simplification,
    Transformation,
)


class TransformationGroup:
    def __init__(self, transformations: Sequence[Transformation]):
        self.transformations = transformations

    def apply_root(self, expr: AstNode) -> bool:
        has_changed = False
        while True:
            changed: bool = False
            for transformation in self.transformations:
                changed = transformation.apply_root(expr) or changed
            has_changed |= changed
            if not changed:
                break
        return has_changed

    def apply_all(self, expr: AstNode) -> bool:
        has_changed = False
        while True:
            changed: bool = False
            for sub_expr in expr:
                changed = self.apply_root(sub_expr) or changed
            has_changed |= changed
            if not changed:
                break
        return has_changed

    def apply2(self, expr: AstNode):
        while True:
            changed: bool = False
            for transformation in self.transformations:
                changed = transformation.apply_all(expr) or changed
            if not changed:
                break

class TransformationPipeline:
    def __init__(self, steps: list[Transformation | TransformationGroup]):
        self.steps = steps

    def apply_all(self, expr: AstNode):
        for step in self.steps:
            step.apply_all(expr)


normalisation_group = TransformationGroup(
        normalisation_patterns +
    [
        Flattening(),
        CanonicalOrdering(),
        Evaluation(),
        Simplification(),
    ]
)

differentiation_group = TransformationGroup(differentiation_rules)

differentiation_pipeline = TransformationPipeline([
    UnFlattening(),
    differentiation_group,
    normalisation_group
    ])
