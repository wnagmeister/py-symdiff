from rules import add_0_rule, mult_0_rule
from astree import AstNode

expr = AstNode.astify_expr("y 0 *")
print(expr)
simplified = mult_0_rule.apply2(expr)
print("\n\n")
print(simplified)
simplified = add_0_rule.apply2(simplified)
print("\n\n")
print(simplified)
