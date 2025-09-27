from rules import add_0_rule, mult_0_rule
from astree import AstNode

expr = AstNode.astify_expr("y 0 * 3 +")
print(expr)
breakpoint()
simplified = mult_0_rule.apply(expr)
print("\n\n")
print(simplified)
