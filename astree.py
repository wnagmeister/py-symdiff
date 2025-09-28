from tree import Node
from symbols import Variable, Operator, operators
from tokens import string_to_tokens, Token, shunting_yard


class AstNode(Node):

    @classmethod
    def astify_rpn(cls, tokens: list[Token]) -> "AstNode":
        """Takes a sequence of tokens in reverse polish notation and returns
        their abstract syntax tree. The constructed children arrays are in the
        same order as the sequence of tokens. Takes optional AstNode arguments
        to substitute in specfied placeholder variable
        """
        stack: list[AstNode] = []
        for token in tokens:
            if isinstance(token, float | Variable):
                stack.append(cls.leafify(token))
            elif isinstance(token, Operator):
                children = [stack.pop() for i in range(token.arity)]
                children.reverse()
                new_node = cls.join(token, children)
                stack.append(new_node)
        return stack.pop()

    @classmethod
    def astify_expr(cls, string: str, notation="r") -> "AstNode":
        return cls.astify_rpn(string_to_tokens(string))

    @classmethod
    def astify(cls, obj: str | float) -> "AstNode":
        """Takes a string expression in infix notation and returns the
        abstract syntax tree."""
        if isinstance(obj, str):
            return cls.astify_rpn(shunting_yard(string_to_tokens(obj)))
        else:
            return cls.leafify(obj)

    # overloading operators to make making new ASTs easier
    def __add__(self, other: "AstNode") -> "AstNode":
        return self.__class__.join(operators.get("+"), [self, other])

    def __mul__(self, other: "AstNode") -> "AstNode":
        return self.__class__.join(operators.get("*"), [self, other])

    def __sub__(self, other: "AstNode") -> "AstNode":
        return self.__class__.join(operators.get("-"), [self, other])

    def __truediv__(self, other: "AstNode") -> "AstNode":
        return self.__class__.join(operators.get("/"), [self, other])

    def __pow__(self, other: "AstNode") -> "AstNode":
        return self.__class__.join(operators.get("^"), [self, other])

    def copy(self) -> "AstNode":
        """Copies the tree. Creates new instances of any variable
        objects in the tree, but retains the existing operator instances
        """
        cls = type(self)
        match self.value:
            case float():
                return cls.leafify(self.value)
            case Variable():
                return cls.leafify(Variable(self.value.string))
            # Operator
            case _:
                children = [child.copy() for child in self.children]
                return cls.join(self.value, children)


if __name__ == "__main__":
    pass
