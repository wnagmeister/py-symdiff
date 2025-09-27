from symbols import Variable
from astree import AstNode


class Rule:

    def __init__(self, pattern: AstNode, replacement: AstNode):
        self.pattern = pattern
        self.replacement = replacement

    # This substitution method does not work for arbitrary variables
    # eg is we have bound f, g, once we replace f, the replacement
    # might contain g's, which we do not want to replace.
    # Better might be a way to find all the nodes(and parents) which
    # need to be replaced, then replace all at once, i.e. no interweaving
    # replacements and searches.
    # or does it work??? once a node is subbed in, its skipped

    def apply(self, expr: AstNode) -> AstNode:
        bindings: dict[Variable, AstNode] = {}
        if is_match(expr, self.pattern, bindings):
            replacement: AstNode = self.replacement.copy()
            substitute(replacement, bindings)
            return replacement
        return expr

    def apply2(self, expr: AstNode) -> AstNode:
        for sub_expr, parent in expr:
            return self.apply(sub_expr)


add_0_rule = Rule(AstNode.astify_expr("f 0 +"), AstNode.astify_expr("f"))
mult_0_rule = Rule(AstNode.astify_expr("f 0 *"), AstNode.astify_expr("0"))


def is_match(
    expr: AstNode, pattern: AstNode, bindings: dict[Variable, AstNode]
) -> bool:  # Unlike in C, the node is never null
    match pattern.value:
        case float():
            return expr.value == pattern.value

        case Variable():
            if existing_binding := bindings.get(
                pattern.value
            ):  # if binding exists, check if expr equals the already bound expression
                return expr.is_equal(existing_binding, lambda x, y: x == y)
            else:  # If not, set new binding
                bindings[pattern.value] = expr
                return True

        case _:  # Operator()
            if expr.value != pattern.value:
                return False
            else:
                for expr_child, pattern_child in zip(expr.children, pattern.children):
                    if not is_match(expr_child, pattern_child, bindings):
                        return False
                return True


def substitute(expr: AstNode, bindings: dict[Variable, AstNode]) -> None:
    """Substitutes variables in expr in place  according to the bindings given."""
    if expr.is_leaf() and (binding := bindings.get(expr.value)):
        expr.value = binding.value
        expr.children = binding.children
    else:
        for i, child in enumerate(expr.children):
            if child.is_leaf():
                if binding := bindings.get(child.value):
                    expr.children[i] = binding
            else:
                substitute(child, bindings)
