from rules import (
    normalise,
    subtraction_removal,
    flatten,
    flatten_recursive,
    sort_commutative,
)
from astree import AstNode

expr = AstNode.astify(" 1 + 5 + x + 3 + exp ( x ) + y - 9 ")
print(expr)
print("\n")
breakpoint()
subtraction_removal.apply_recursive(expr)
flatten_recursive(expr)
print(expr)
print("\n")
sort_commutative(expr)
print(expr)
