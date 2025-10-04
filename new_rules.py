from symbols import Operator, Variable, operators
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
    """Evaluates an expression for concrete operators. Assumes that the
    expression has been normalised with all subtractions and divisions replaced
    with addition and multiplication, summands and factors have been ordered,
    and that expressions with zero or one summand/factor which is a float have
    been folded into the operator in the identity simplification phase.
    """

    def apply_root(self, expr: AstNode) -> bool:
        if (
            isinstance(expr.value, Operator)
            and expr.value.func
            and expr.value.arity <= (num := self.num_floats(expr.children))
        ):
            if expr.value.arity == 1:
                expr.value = expr.value.func(expr.children.pop(0).value)
                expr.children = []
            else:
                result: float = expr.value.func(
                    expr.children.pop(0).value, expr.children.pop(0).value
                )
                for i in range(num - 2):
                    result = expr.value.func(result, expr.children.pop(0).value)
                if expr.num_children() > 0:
                    expr.children.insert(0, AstNode.leafify(result))
                else:  # num < expr.num_children()
                    expr.value = result
                    expr.children = []
            return True
        else:
            return False

    @staticmethod
    def num_floats(nodes: list[AstNode]) -> int:
        """Finds the number of nodes in a list which contain float values."""
        num: int = 0
        for node in nodes:
            if isinstance(node.value, float):
                num += 1
        return num


class Simplification(Transformation):
    def apply_root(self, expr: AstNode) -> bool:
        """If no summands/factors left, replaces expr with the identity of the
        operator. If exactly one summand/factor left, folds it into the
        operator.
        """
        if expr.value == operators["+"]:
            old_length: int = expr.num_children()
            expr.children[:] = [child for child in expr.children if child.value != 0]
            if expr.num_children() == 0:
                expr.value == 0.0
                return True
            elif expr.num_children() == 1:
                expr.value == expr.children.pop()
                return True
            else:
                return old_length == expr.num_children()

        elif expr.value == operators["*"]:
            if 0.0 in [child.value for child in expr.children]:
                expr.value = 0.0
                expr.children = []
                return True
            old_length: int = expr.num_children()
            expr.children[:] = [child for child in expr.children if child.value != 1]
            if expr.num_children() == 0:
                expr.value == 1.0
                return True
            elif expr.num_children() == 1:
                expr.value == expr.children.pop()
                return True
            else:
                return old_length == expr.num_children()
        return False


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
        self.name = (name,)
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
    def apply_root(self, expr: AstNode):
        pass


if __name__ == "__main__":
    pass
