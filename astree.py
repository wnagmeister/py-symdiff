from tree import TNode
from symbols import Variable, Operand, Operator, operators
from tokens import string_to_tokens


class AstNode(TNode):

    @classmethod
    def astify_rpn(
        cls,
        tokens: list[Operand | Operator],
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
            if isinstance(token, Operand):
                if token.is_optype(Variable) and token.opvalue.equals(placeholder):  # type: ignore
                    stack.append(args[n])
                    n += 1
                else:
                    stack.append(cls.nodify(token))

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
            return cls.nodify(Operand(Variable(const)))
        return cls.nodify(Operand(const))

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
            if self.value.is_optype(Variable):
                return x
            return self.value.opvalue
        return self.value.func(*([child.evaluate(x) for child in self.children]))

    def eval2(self, x: float, var=Variable("x")) -> "AstNode":
        """sets all appearances of var x to value x"""
        if self.value.is_optype(Variable) and self.value.opvalue.equals(var):
            return self.astify_const(x)
        return self.__class__.create_node(
            self.value, [self.eval2(x, var=var) for child in self.children]
        )

    def simplify_const(self):
        """simplify constant expressions: 1 2 + -> 3"""
        pass

    def _diff_depr(self, wrt: Variable = Variable("x")) -> "AstNode":

        if self.is_leaf():
            if self.value.is_optype(Variable) and self.value.opvalue.equals(wrt):
                return self.astify_const(1)
            return self.astify_const(0)

        if self.value == operators.get("+"):
            return diff_add(self)
        elif self.value == operators.get("*"):
            return diff_mult(self)
        elif self.value == operators.get("/"):
            return diff_div(self)

        return self.nodify(Operand(0))

    def derivative(self, wrt: Variable = Variable("x")) -> "AstNode":

        if self.is_leaf():
            if self.value.is_optype(Variable) and self.value.opvalue.equals(wrt):
                return self.__class__.astify_const(1)
            return self.__class__.astify_const(0)

        return self.diff_str_to_op(self.value.diff)(self)

    def d(self, wrt=Variable("x")):
        return self.derivative(wrt=wrt)

    def prune(self) -> "AstNode":
        """simple prune of the tree"""
        if self.is_leaf():
            return self
        elif self.no_of_child_leaves() > 0:
            match self.value.string:
                case "+":
                    for i, child in enumerate(self.children):
                        if (
                            isinstance(child.value, Operand)
                            and not child.value.is_optype(Variable)
                            and child.value.opvalue == 0
                        ):
                            if i == 0:
                                return self.children[1]
                            if i == 1:
                                return self.children[0]
                case "-":
                    for i, child in enumerate(self.children):
                        if (
                            isinstance(child.value, Operand)
                            and not child.value.is_optype(Variable)
                            and child.value.opvalue == 0
                        ):
                            if i == 0:
                                return self.__class__.astify_format(
                                    "-1 {} *", self.children[1]
                                )
                            if i == 1:
                                return self.children[0]
                case "*":
                    for child in self.children:
                        if (
                            isinstance(child.value, Operand)
                            and not child.value.is_optype(Variable)
                            and child.value.opvalue == 0
                        ):
                            return self.__class__.astify_const(0)

                    for i, child in enumerate(self.children):
                        if (
                            isinstance(child.value, Operand)
                            and not child.value.is_optype(Variable)
                            and child.value.opvalue == 1
                        ):
                            if i == 0:
                                return self.children[1]
                            if i == 1:
                                return self.children[0]

                case "/":
                    numerator = self.children[0]
                    if (
                        isinstance(numerator.value, Operand)
                        and not numerator.value.is_optype(Variable)
                        and numerator.value.opvalue == 0
                    ):
                        return self.__class__.astify_const(0)
        return self.__class__.create_node(
            self.value, [child.prune() for child in self.children]
        )

    @classmethod
    def diff_str_to_op(cls, diff_str: str):
        """converts diff string of an operator into the differentiation function
        of ASTs that returns ASTs"""
        str_tokens = diff_str.split()
        """replaces all a0 a1 a2 d0 d1 d2 with the placeholder {}"""
        format_tokens = ["{}" if token[0] == "#" else token for token in str_tokens]
        format_str = " ".join(format_tokens)

        """retrieves indices of substitution nodes in diff string, indices >= 0
        so we invert them across i=-0.5 to indicate that the node should be
        differentiated"""
        child_tokens = [token for token in str_tokens if token[0] == "#"]
        child_nodes = [
            -int(token[2:]) - 1 if (token[1] == "#") else int(token[1:])
            for token in child_tokens
        ]

        def diff_op(ast: AstNode) -> AstNode:
            """Potential list mutability problems"""
            return cls.astify_format(
                format_str,
                *[
                    (
                        ast.children[i]
                        if i >= 0
                        else cls.derivative(ast.children[-(i + 1)])
                    )
                    for i in child_nodes
                ],
            )

        return diff_op


if __name__ == "__main__":
    pass
