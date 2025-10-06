from symbols import Operator, Variable, operators
from astree import AstNode
from typing import Callable


# TODO: replace: expr.value = other.value, expr.children = other.children with
# a unified susbtitution mechanism which does not erase expr.


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
    def apply_root(self, expr: AstNode) -> bool:
        if isinstance(expr.value, Operator) and expr.value.commutative:
            expr_children_copy = expr.children[:]
            expr.children.sort(key=self.expr_sort_key)
            return expr_children_copy != expr.children
        else:
            return False

    @staticmethod
    def expr_sort_key(expr: AstNode) -> tuple[int, float | str | int]:
        match expr.value:
            case float():
                return (0, expr.value)
            case Variable():
                return (1, expr.value.string)
            case Operator():
                return (2, expr.value.precedence)
            case _:
                raise TypeError


class Evaluation(Transformation):
    """Evaluates an expression for concrete operators. Assumes that the
    expression has been normalised with all subtractions and divisions replaced
    with addition and multiplication, summands and factors have been ordered,
    and that expressions with zero or one summand/factor which is a float have
    been folded into the operator in the identity simplification phase.
    """
    pass




    @staticmethod
    def num_floats(nodes: list[AstNode]) -> int:
        """Finds the number of nodes in a list which contain float values."""
        num = 0
        for node in nodes:
            if isinstance(node.value, float):
                num += 1
        return num


class Simplification(Transformation):
    # Does not require flattening to work?
    def apply_root(self, expr: AstNode) -> bool:
        """If no summands/factors left, replaces expr with the identity of the
        operator. If exactly one summand/factor left, folds it into the
        operator.
        """
        if expr.value == operators["+"]:
            old_length = expr.num_children()
            expr.children[:] = [child for child in expr.children if child.value != 0]
            if expr.num_children() == 0:
                expr.value = 0.0
                return True
            elif expr.num_children() == 1:
                expr.value = expr.children[0].value
                expr.children = expr.children[0].children
                return True
            else:
                return old_length == expr.num_children()

        elif expr.value == operators["*"]:
            if 0.0 in [child.value for child in expr.children]:
                expr.value = 0.0
                expr.children = []
                return True
            old_length = expr.num_children()
            expr.children[:] = [child for child in expr.children if child.value != 1]
            if expr.num_children() == 0:
                expr.value = 1.0
                return True
            elif expr.num_children() == 1:
                expr.value = expr.children[0].value
                expr.children = expr.children[0].children
                return True
            else:
                return old_length == expr.num_children()
        return False


if __name__ == "__main__":
    pass
