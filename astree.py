from tree import Node
from symbols import Variable, Operator
from tokens import string_to_tokens, Token


class AstNode(Node):

    @classmethod
    def astify_rpn(
        cls,
        tokens: list[Token],
        *args: "AstNode",
        placeholder: Variable = Variable("{}"),
    ) -> "AstNode":
        """Takes a sequence of tokens in reverse polish notation and returns
        their abstract syntax tree. The constructed children arrays are in the
        same order as the sequence of tokens. Takes optional AstNode arguments
        to substitute in specfied placeholder variable
        """
        n: int = 0  # variable args counter
        stack: list[AstNode] = []
        for token in tokens:
            if isinstance(token, float | Variable):
                if isinstance(token, Variable) and token == placeholder:
                    stack.append(args[n])
                    n += 1
                else:
                    stack.append(cls.leafify(token))

            elif isinstance(token, Operator):
                children = [stack.pop() for i in range(token.arity)]
                children.reverse()
                new_node = cls.create_node(token, children)
                stack.append(new_node)
        return stack.pop()

    @classmethod
    def astify_expr(cls, string: str, notation="r") -> "AstNode":
        return cls.astify_rpn(string_to_tokens(string))

    @classmethod
    def astify_const(cls, const: float | str) -> "AstNode":
        if isinstance(const, str):
            return cls.leafify((Variable(const)))
        return cls.leafify((const))

    @classmethod
    def astify_format(cls, string: str, *args):
        """creates an AstNode based on a formatted input. Eg:
        astify_format("{} {} +", tree0, tree1))  creates a tree consisting of
        the sum of tree0 and tree1, variable nodes of form {} be replaced by
        the arbitrary arguments of astify_format TODO - make it work like
        string.format()
        implementation idea: traverse tree, find leaves of {n}form, replace in
        place requires tree traversal search algs tho

        currently just does reversepolishtotree modified
        """
        return cls.astify_rpn(
            string_to_tokens(string), *args, placeholder=Variable("{}")
        )

    @classmethod
    def astify(cls, obj: str | float, *args, notation="r") -> "AstNode":
        if isinstance(obj, str):
            return cls.astify_format(obj, *args)
        else:
            return cls.astify_const(obj)

    # overloading operators to make making new ASTs easier
    def __add__(self, ast: "AstNode") -> "AstNode":
        return self.__class__.astify_format("{} {} +", self, ast)

    def __mul__(self, ast: "AstNode") -> "AstNode":
        return self.__class__.astify_format("{} {} *", self, ast)

    def __sub__(self, ast: "AstNode") -> "AstNode":
        return self.__class__.astify_format("{} {} -", self, ast)

    def __truediv__(self, ast: "AstNode") -> "AstNode":
        return self.__class__.astify_format("{} {} /", self, ast)

    def __pow__(self, ast: "AstNode") -> "AstNode":
        return self.__class__.astify_format("{} {} ^", self, ast)

    def evaluate(self, x: float) -> float:
        """evaluates the AST, sets all variables to x"""
        if self.is_leaf():
            if isinstance(self.value, Variable):
                return x
            return self.value
        return self.value.func(*([child.evaluate(x) for child in self.children]))

    def eval2(self, x: float, var=Variable("x")) -> "AstNode":
        """sets all appearances of var x to value x"""
        if self.value.is_optype(Variable) and self.value.opvalue.equals(
            var
        ):  # remove optype
            return self.astify_const(x)
        return self.__class__.create_node(
            self.value, [self.eval2(x, var=var) for child in self.children]
        )

    def copy(self) -> "AstNode":
        """Copies the tree. Creates new instances of any variable objects in the tree, but retains the existing operator instances."""
        cls = type(self)
        match self.value:
            case float():
                return cls.leafify(self.value)
            case Variable():
                return cls.leafify(Variable(self.value.string))
            case _:  # Operator()
                children = [child.copy() for child in self.children]
                return cls.create_node(self.value, children)


if __name__ == "__main__":
    pass
