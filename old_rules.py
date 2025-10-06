from symbols import Variable, Operator, operators
from astree import AstNode


class PatternVariable(Variable):
    def __init__(self, string: str, match_type: None | float = None):
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
    def make_patt(cls, expr: AstNode) -> None:
        """Replaces all the Variables in a AST with PatternVariables, with match typed inferred as usual."""
        # for sub_expr in expr:
        # if isinstance(sub_expr.value, Variable):
        #     sub_expr.value = cls(sub_expr.value.string)
        substitutions = {
            var: AstNode.leafify(PatternVariable(var.string))
            for var in expr.variables()
        }
        expr.substitute_variables(substitutions)


class Rule:
    """Transformation rule for AstNode trees."""

    def __init__(self, name: str, pattern: AstNode, replacement: AstNode):
        self.name = name
        self.pattern = pattern
        self.replacement = replacement

    def apply(self, expr: AstNode) -> bool:
        """Applies the rule in place onto the expression expr if possible. The
        rule must match to the whole of expr; it does not match it to
        subexpressions. At the end, returns True if expr was modified, False if
        not.
        """
        bindings: dict[Variable, AstNode] = {}
        if is_match(expr, self.pattern, bindings):
            replacement: AstNode = self.replacement.copy()
            replacement.substitute_variables(bindings)
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
    expr: AstNode, pattern: AstNode, bindings: dict[PatternVariable, AstNode]
) -> bool:
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


def match2(
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
                for expr_child, pattern_child in zip(expr.children, pattern.children):
                    if not is_match(expr_child, pattern_child, bindings):
                        return False
                return True


rules: set[Rule] = {
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
            if len(sub_expr.children) < 2:
                sub_expr.value = sub_expr.children[0].value
                sub_expr.children = sub_expr.children[0].children
    return changed


def multiplicative_identity(expr: AstNode) -> bool:
    changed: bool = False
    for sub_expr in expr:
        if sub_expr.value == operators["*"] and (old_length := len(sub_expr.children)):
            sub_expr.children[:] = [
                child for child in sub_expr.children if child.value != 1
            ]
            changed = old_length != len(sub_expr.children) or changed
            if len(sub_expr.children) < 2:
                sub_expr.value = sub_expr.children[0].value
                sub_expr.children = sub_expr.children[0].children
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
