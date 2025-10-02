from symbols import Operator, Variable
from astree import AstNode
from typing import cast


class Transformation:
    """AST transformations base class. Transfomation application must be
    implemented by subclasses.
    """

    def __init__(self):
        pass

    def apply_root(self, expr: AstNode) -> bool:
        """Implementations should apply the transformation strictly to the
        expression rooted at expr. The apply_all method will handle the
        recursion.
        """
        raise NotImplementedError

    def apply_all(self, expr: AstNode) -> bool:
        """Recursively applies the transformation bottom up in post-order."""
        applied = False
        for sub_expr in expr:
            applied |= self.apply_root(sub_expr) or applied
        return applied


class Flattening(Transformation):
    def apply_root(self, expr: AstNode) -> bool:
        applied: bool = False
        if isinstance(expr.value, Operator) and expr.value.associative == "full":
            new_children: list[AstNode] = []
            for sub_expr in expr.children:
                if expr.value == sub_expr.value:
                    new_children.extend(sub_expr.children)
                    applied = True
                else:
                    new_children.append(sub_expr)
            expr.children = new_children
        return applied


class CanonicalOrdering(Transformation):
    @staticmethod
    def expr_sort_key(expr: AstNode) -> tuple[int, float | str | int]:
        match expr.value:
            case float():
                return (0, expr.value)
            case Variable():
                return (1, expr.value.string)
            case _:  # case Operator():
                return (2, expr.value.precedence)

    def apply_root(self, expr: AstNode) -> bool:
        if isinstance(expr.value, Operator) and expr.value.commutative:
            expr_children_copy = expr.children[:]
            expr.children.sort(key=self.expr_sort_key)
            return expr_children_copy != expr.children
        else:
            return False


class Evaluation(Transformation):
    def apply_root(self, expr: AstNode) -> bool:
        applied = False
        if isinstance(expr.value, Operator) and expr.value.func:
            number: None | float = None
            match expr.value.arity:
                case 1:
                    if isinstance(expr.children[0].value, float):
                        number = expr.value.func(expr.children[0].value)
                case 2:
                    numbers = [
                        node for node in expr.children if isinstance(node.value, float)
                    ]
                    rest = [node for node in expr.children if node not in numbers]
                    for node in numbers:
                        if number is None:
                            number = node.value
                        else:
                            number = expr.value.func(number, node.value)
                    if number is not None:
                        rest.append(AstNode.leafify(number))

            if len(rest) != expr.num_children():
                applied = True
            expr.children = rest
            if expr.num_children() == 1:
                expr.value = expr.children[0].value
                expr.children = expr.children[0].children
        return applied


class Simplification(Transformation):
    pass


class PatternVariable(Variable):
    def __init__(self, string, match_type: None | float = None):
        """If a match type is not given, it is inferred from the string."""
        super().__init__(string)
        if not match_type:
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
        """Replaces all the Variables in a AST with PatternVariables, with match_type inferred as usual."""
        substitutions = {
            var: AstNode.leafify(PatternVariable(var.string))
            for var in expr.variables()
        }
        expr.substitute_variables(substitutions)


class PatternMatching(Transformation):
    def __init__(self, name: str, pattern: AstNode, replacement: AstNode):
        self.name = (name,)
        self.pattern = pattern
        self.replacement = replacement

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

            case _:
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
    def apply_root(self, expr: AstNode):
        pass


if __name__ == "__main__":
    pass
