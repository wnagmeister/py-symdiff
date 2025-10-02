from symbols import Variable, Operator, operators
from astree import AstNode


class PatternVariable(Variable):
    def __init__(self, string, match_type=None):
        super().__init__(string)
        if not match_type:
            self.match_type = self.default_match_type(string)

    @staticmethod
    def default_match_type(string: str):
        match string:
            case "s":
                return float
            case "o":
                return Operator
            case "v":
                return Variable
            case "l":
                return "literal"
            case _:
                return "all"


class Rule:
    """Transformation rule for AstNode trees."""

    def __init__(self, name: str, pattern: AstNode, replacement: AstNode):
        self.name = name
        self.pattern = pattern
        self.replacement = replacement

    # This substitution method does not work for arbitrary variables
    # eg is we have bound f, g, once we replace f, the replacement
    # might contain g's, which we do not want to replace.
    # Better might be a way to find all the nodes(and parents) which
    # need to be replaced, then replace all at once, i.e. no interweaving
    # replacements and searches.
    # or does it work??? once a node is subbed in, its skipped

    def apply(self, expr: AstNode) -> bool:
        """Applies the rule in place onto the expression expr if possible. The
        rule must match to the whole of expr; it does not match it to
        subexpressions. At the end, returns True if expr was modified, False if
        not.
        """
        bindings: dict[Variable, AstNode] = {}
        if is_match(expr, self.pattern, bindings):
            replacement: AstNode = self.replacement.copy()
            substitute(replacement, bindings)
            expr.value = replacement.value
            expr.children = replacement.children
            return True
        else:
            return False

    def apply_recursive(self, expr: AstNode) -> bool:
        """Applies the rule in place to the expression expr. Will iterate
        recursively over subexpressions, and attempt to apply the rule on each one
        if possible. Returns True if expr was modified, False if not.
        """
        changed: bool = False
        for sub_expr in expr:
            changed = self.apply(sub_expr) or changed
        return changed


def apply_all_rules(expr: AstNode) -> None:
    """Continuously applies every rule in the rules dictionary onto the
    expression. Stops when every rule has been applied twice without any effect.
    """
    prev_changed: bool = False
    while True:
        changed: bool = False
        for rule in rules:
            changed = rule.apply_recursive(expr) or changed
        if not prev_changed and not changed:
            break
        else:
            prev_changed = changed


def is_match(
    expr: AstNode, pattern: AstNode, bindings: dict[Variable, AstNode]
) -> bool:
    """Checks if expr matches the pattern given. All variables in
    pattern are wildcards which can be bound to any subexpression.
    Will only return True if the entire expression matches the pattern;
    it will not match subexpressions of expr to the pattern.
    """
    match pattern.value:
        case float():
            return expr.value == pattern.value

        case Variable():
            if existing_binding := bindings.get(pattern.value):
                # If a variable is bound, check if the bound expression is the
                # same as the currently matched expression
                return expr.is_equal(existing_binding, lambda x, y: x == y)
            else:
                bindings[pattern.value] = expr
                return True

        case _:  # case: Operator()
            if not isinstance(expr.value, Operator) or expr.value != pattern.value:
                return False
            else:
                for expr_child, pattern_child in zip(expr.children, pattern.children):
                    if not is_match(expr_child, pattern_child, bindings):
                        return False
                return True


def substitute(expr: AstNode, bindings: dict[Variable, AstNode]) -> None:
    """Substitutes variables in expr in place according to the bindings
    given.
    """
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


rules: set[Rule] = {
    Rule("Add 0 1", AstNode.astify("f + 0"), AstNode.astify("f")),
    Rule("Add 0 2", AstNode.astify("0 + f"), AstNode.astify("f")),
    Rule("Multiply 0 1", AstNode.astify("f * 0"), AstNode.astify("0")),
    Rule("Multiply 0 2", AstNode.astify("0 * f"), AstNode.astify("0")),
    Rule("Multiply 1 1", AstNode.astify("f * 1"), AstNode.astify("f")),
    Rule("Multiply 1 2", AstNode.astify("1 * f"), AstNode.astify("f")),
    Rule("x + x = 2x", AstNode.astify("f + f"), AstNode.astify("2 * f")),
    Rule("Derivative w.r.t itself", AstNode.astify("f D f"), AstNode.astify("1")),
    Rule(
        "Product rule",
        AstNode.astify_expr("x f g * D"),
        AstNode.astify_expr("x f D g * f x g D * +"),
    ),
    Rule(
        "Derivative of exp",
        AstNode.astify_expr("x f exp D"),
        AstNode.astify_expr("f exp x f D *"),
    ),
}


def normalise(expr: AstNode):
    subtraction_removal.apply_recursive(expr)
    flatten_recursive(expr)
    sort_commutative(expr)
    apply_identities(expr)


subtraction_removal: Rule = Rule(
    "subtraction to multiplication by -1",
    AstNode.astify("f - g"),
    AstNode.astify("f + ( -1 * g )"),
)


def flatten(expr: AstNode) -> bool:
    """Flattens the operator at the root of expr with any of its immediate
    children if possible.
    """
    flattened: bool = False
    if isinstance(expr.value, Operator) and expr.value.associative == "full":
        new_children: list[AstNode] = []
        for sub_expr in expr.children:
            if expr.value == sub_expr.value:
                new_children.extend(sub_expr.children)
                flattened = True
            else:
                new_children.append(sub_expr)
        expr.children = new_children
    return flattened


def flatten_recursive(expr: AstNode) -> bool:
    """Recursively flattens any operators in expr with any immediate children if
    possible."""
    flattened: bool = False
    for sub_expr in expr:
        flattened = flatten(sub_expr) or flattened
    return flattened


def expr_sort_key(expr: AstNode) -> tuple[int, float | str | int]:
    match expr.value:
        case float():
            return (0, expr.value)
        case Variable():
            return (1, expr.value.string)
        case _:  # case Operator():
            return (2, expr.value.precedence)


def sort_commutative(expr: AstNode) -> None:
    for sub_expr in expr:
        if isinstance(sub_expr.value, Operator) and sub_expr.value.commutative:
            sub_expr.children.sort(key=expr_sort_key)


def additive_identity(expr: AstNode) -> bool:
    changed: bool = False
    for sub_expr in expr:
        if sub_expr.value == operators["+"] and (old_length := len(sub_expr.children)):
            sub_expr.children[:] = [
                child for child in sub_expr.children if child.value != 0
            ]
            changed = old_length != len(sub_expr.children) or changed
    return changed


def multiplicative_identity(expr: AstNode) -> bool:
    changed: bool = False
    for sub_expr in expr:
        if sub_expr.value == operators["*"] and (old_length := len(sub_expr.children)):
            sub_expr.children[:] = [
                child for child in sub_expr.children if child.value != 1
            ]
            changed = old_length != len(sub_expr.children) or changed
    return changed


def multiplication_zero(expr: AstNode) -> bool:
    changed: bool = False
    for sub_expr in expr:
        if sub_expr.value == operators["*"]:
            for child in sub_expr.children:
                if child.value == 0:
                    sub_expr.value = 0.0
                    sub_expr.children = []
                    changed = True
                    break
    return changed


def apply_identities(expr: AstNode) -> None:
    for sub_expr in expr:
        changed = False
        while True:
            changed = additive_identity(sub_expr) or changed
            changed = multiplicative_identity(sub_expr) or changed
            changed = multiplication_zero(sub_expr) or changed
            if not changed:
                break


if __name__ == "__main__":
    pass
