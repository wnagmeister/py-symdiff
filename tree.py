class Node:

    nodewidth = 5

    def __init__(self, value, children: list):
        self.value = value
        self.children = children
        self.num_children = len(children)

    @classmethod
    def create_node(cls, value, children: list):
        return cls(value, children)

    @classmethod
    def leafify(cls, value):
        """Returns a leaf node with value value and no children"""
        return cls(value, [])

    def is_leaf(self) -> bool:
        if not self.children:
            return True
        return False

    def no_of_child_leaves(self) -> int:  # Why is this a method?
        """counts the number of children which are leaves"""
        n = 0
        for child in self.children:
            if child.is_leaf():
                n += 1
        return n

    def flatten(self, child) -> "Node":  # Is this method even used?
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
            return (
                max(child.height() for child in self.children) + 1
            )  # Stack overflow possibility

    def _add_child(self, new_child):
        self.children.append(new_child)
        self.num_children = len(self.children)

    def is_equal(self, other: "Node", compare) -> bool:
        if self.is_leaf() ^ other.is_leaf():
            return False
        elif self.num_children != other.num_children:
            return False
        elif not compare(self.value, other.value):
            return False
        else:
            for self_child, other_child in zip(self.children, other.children):
                if not self_child.is_equal(other_child, compare):
                    return False
            return True

    @staticmethod
    def pad_para(
        para: str, char: str = " "
    ) -> str:  # Tree printing methods should go outside class definition
        """left-pads every line in a multi-line string by nodewidth many char"""
        return "\n".join(
            [(Node.nodewidth) * char + line for line in para.split(sep="\n")]
        )

    @staticmethod
    def make_branch(string: str) -> str:
        return "|" + string.rjust(Node.nodewidth, "-")

    def __repr__(self):
        if self.is_leaf():
            return Node.make_branch(repr(self.value))

        lst = []
        for i, child in enumerate(self.children):
            if i == self.num_children // 2:
                lst.append(Node.make_branch(repr(self.value)))
            lst.append(Node.pad_para(repr(child)))
        return "\n".join(lst)


if __name__ == "__main__":
    pass
