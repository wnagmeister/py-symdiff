from rules import apply_all_rules
from astree import AstNode
from symbols import operators

expr = AstNode.astify_expr("1 0 * 4 + 0 x + 0 * +")
print(expr)
apply_all_rules(expr)
print("\n")
print(expr)
print("\n\n")

expr2 = AstNode.astify_expr("x 2 x * D")
print(expr2)
apply_all_rules(expr2)
print("\n")
print(expr2)
print("\n\n")

expr3 = AstNode.astify_expr("x 2 x * exp D")
print(expr3)
apply_all_rules(expr3)
print("\n\n\n")
print(expr3)
