from tree import Node
from symbols import Variable, Operator, operators
from tokens import string_to_tokens, Token, shunting_yard
from typing import Self


class AstNode(Node[Token]):
    """Abstract syntax tree for mathematical expressions."""

    @classmethod
    def astify_rpn(cls, tokens: list[Token]):
        """Takes a sequence of tokens in reverse polish notation and returns
        their AST. The constructed children arrays are in the same order as the
        sequence of tokens.
        """
        stack: list[AstNode] = []
        for token in tokens:
            if isinstance(token, float | Variable):
                stack.append(cls.leafify(token))
            elif isinstance(token, Operator):
                children = [stack.pop() for _ in range(token.arity)]
                children.reverse()
                new_node = cls(token, children)
                stack.append(new_node)
        return stack.pop()

    @classmethod
    def astify_expr(cls, string: str):
        """Astify but for reverse Polish notation."""
        return cls.astify_rpn(string_to_tokens(string))

    @classmethod
    def astify(cls, obj: str | float):
        """Takes a string expression in infix notation and returns the AST. The
        main AST making function."""
        if isinstance(obj, str):
            return cls.astify_rpn(shunting_yard(string_to_tokens(obj)))
        else:
            return cls.leafify(obj)

    """Overloading operators to make making new ASTs easier."""

    def __add__(self, other: Self):
        return self.__class__(operators["+"], [self, other])

    def __mul__(self, other: Self):
        return self.__class__(operators["*"], [self, other])

    def __sub__(self, other: Self):
        return self.__class__(operators["-"], [self, other])

    def __truediv__(self, other: Self):
        return self.__class__(operators["/"], [self, other])

    def __pow__(self, other: Self):
        return self.__class__(operators["^"], [self, other])

    def copy(self) -> Self:
        """Copies the tree. Creates new instances of any variable
        objects in the tree, but retains the existing operator instances.
        """
        cls = self.__class__
        match self.value:
            case float():
                return cls.leafify(self.value)
            case Variable():
                return cls.leafify(Variable(self.value.string))
            case Operator():
                return cls(self.value, [child.copy() for child in self.children])
            case _:
                raise TypeError
    
    


    def variables(self) -> set[Variable]:
        variables: set[Variable] = set()
        for node in self:
            if isinstance(node.value, Variable):
                variables.add(node.value)
        return variables

    def substitute_variables(self, substitutions: dict[Variable, "AstNode"]) -> None:
        for node in self:
            if isinstance(node.value, Variable) and (substitution := substitutions.get(node.value)):
                node.value = substitution.value
                node.children = substitution.children


if __name__ == "__main__":
    pass
