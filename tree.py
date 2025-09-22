class TNode:

    nodewidth = 5

    def __init__(self, value, children: list):
        self.value = value
        self.children = children
        self.no_of_children = len(children)

    @classmethod
    def create_node(cls, value, children: list):
        return cls(value, children)

    @classmethod
    def nodify(cls, value):
        """Returns a leaf node with value value and no children"""
        return cls(value, [])

    def is_leaf(self):
        if not self.children:
            return True
        return False

    def no_of_child_leaves(self) -> int:
        """counts the number of children which are leaves"""
        n = 0
        for child in self.children:
            if child.is_leaf():
                n += 1
        return n

    def flatten(self, child) -> "TNode":
        """removes the given child node and adds the children of the child
        directly to the children of self"""
        # assert the child is child of self
        # i can FEEL the mutability problems
        new_children = [
            other for other in self.children if other != child
        ] + child.children
        return self.__class__.create_node(self.value, new_children)

    def height(self) -> int:
        if self.is_leaf():
            return 0
        else:
            return max(child.height() for child in self.children) + 1

    def _add_child(self, new_child):
        self.children.append(new_child)
        self.no_of_children = len(self.children)

    @staticmethod
    def pad_para(para: str, char: str = " ") -> str:
        """left-pads every line in a multi-line string by nodewidth many char"""
        return "\n".join(
            [(TNode.nodewidth) * char + line for line in para.split(sep="\n")]
        )

    @staticmethod
    def make_branch(string: str) -> str:
        return "|" + string.rjust(TNode.nodewidth, "-")

    def __repr__(self):
        if self.is_leaf():
            return TNode.make_branch(repr(self.value))

        lst = []
        for i, child in enumerate(self.children):
            if i == self.no_of_children // 2:
                lst.append(TNode.make_branch(repr(self.value)))
            lst.append(TNode.pad_para(repr(child)))
        return "\n".join(lst)


if __name__ == "__main__":
    pass
