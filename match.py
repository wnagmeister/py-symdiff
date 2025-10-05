from symbols import Variable, Operator
from astree import AstNode
from rules import Transformation
from typing import cast


class PatternVariable(Variable):
    def __init__(self, string: str, match_type: None | float = None):
        """If a match type is not given, it is inferred from the string."""
        super().__init__(string)
        self.match_type = match_type
        if not self.match_type:
            self.match_type = self.default_match_type(string)

    @staticmethod
    def default_match_type(string: str):
        match string:
            case "s":
                return float
            case _:
                return "all"

    def match(self, expr: AstNode) -> bool:
        """Returns whether the PatternVariable matches expr at the root."""
        if self.match_type == "all":
            return True
        else:
            return isinstance(expr.value, self.match_type)

    @classmethod
    def patternify(cls, expr: AstNode) -> None:
        """Replaces all the non-Pattern Variables in a AST with
        PatternVariables, with match_type inferred as usual.
        """
        substitutions = {
            var: AstNode.leafify(PatternVariable(var.string))
            for var in expr.variables()
            if not isinstance(var, PatternVariable)
        }
        expr.substitute_variables(substitutions)


class PatternMatching(Transformation):
    def __init__(self, name: str, pattern: AstNode, replacement: AstNode):
        self.name = name
        self.pattern = pattern
        self.replacement = replacement
        PatternVariable.patternify(self.pattern)
        PatternVariable.patternify(self.replacement)

    def apply_root(self, expr: AstNode):
        """Applies the transformation in place onto the root of expr if able."""
        bindings: dict[PatternVariable, AstNode] = {}
        if PatternMatching.match(expr, self.pattern, bindings):
            replacement = self.replacement.copy()
            replacement.substitute_variables(cast(dict[Variable, AstNode], bindings))
            expr.value = replacement.value
            expr.children = replacement.children
            return True
        else:
            return False

    @staticmethod
    def match(
        expr: AstNode, pattern: AstNode, bindings: dict[PatternVariable, AstNode]
    ) -> bool:
        match pattern.value:
            case float():
                return expr.value == pattern.value

            case PatternVariable():
                if pattern.value.match_type == "all" or isinstance(
                    expr.value, pattern.value.match_type
                ):
                    if existing_binding := bindings.get(pattern.value):
                        return expr.is_equal(existing_binding)
                    else:
                        bindings[pattern.value] = expr
                        return True
                else:
                    return False

            case Variable():
                return expr.value == pattern.value

            case _:  # Operator():
                if not isinstance(expr.value, Operator) or expr.value != pattern.value:
                    return False
                else:
                    for expr_child, pattern_child in zip(
                        expr.children, pattern.children
                    ):
                        if not PatternMatching.match(
                            expr_child, pattern_child, bindings
                        ):
                            return False
                    return True


class Differentiation(PatternMatching):
    pass


normalisation_rules = [
    PatternMatching("- to +", AstNode.astify("f - g"), AstNode.astify("f + ( -1 * g )"))
]

differentiation_rules = [
    Differentiation("constant", AstNode.astify("x D s"), AstNode.astify("0")),
    Differentiation("variable", AstNode.astify("x D x"), AstNode.astify("1")),
    Differentiation(
        "sum rule",
        AstNode.astify("x D ( f + g )"),
        AstNode.astify("( x D f ) + ( x D g )"),
    ),
    Differentiation(
        "product rule",
        AstNode.astify("x D ( f * g )"),
        AstNode.astify("( ( x D f ) * g ) + ( f * ( x D g ) )"),
    ),
]

if __name__ == "__main__":
    pass
