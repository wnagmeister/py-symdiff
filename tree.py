from typing import Callable, Generator, Generic, Self, TypeVar

T = TypeVar("T")


class Node(Generic[T]):
    """Generic (arbitrary number of children) tree data structure."""

    nodewidth = 5

    def __init__(self, value: T, children: list[Self]):
        self.value = value
        self.children = children

    @classmethod
    def leafify(cls, value: T):
        """Returns a leaf node with value value and no children."""
        return cls(value, [])

    def is_leaf(self) -> bool:
        if not self.children:
            return True
        return False

    def height(self) -> int:
        if self.is_leaf():
            return 0
        else:
            return max(child.height() for child in self.children) + 1

    def num_children(self) -> int:
        return len(self.children)

    def is_equal(
        self, other: Self, compare: Callable[[T, T], bool] = lambda x, y: x == y
    ) -> bool:
        """Compares two trees for equality. Two node values are equal if the
        given compare function (default __eq__) for node values agrees."""
        if self.is_leaf() ^ other.is_leaf():
            return False
        elif self.num_children() != other.num_children():
            return False
        elif not compare(self.value, other.value):
            return False
        else:
            for self_child, other_child in zip(self.children, other.children):
                if not self_child.is_equal(other_child, compare):
                    return False
            return True

    def traverse(self) -> Generator[Self]:
        """Traverses over the subnodes in post-order."""
        for child in self.children:
            yield from child.traverse()
        yield self

    def __iter__(self):
        """Iterates over the subnodes in post-order."""
        return self.traverse()

    """"Tree printing methods"""

    @staticmethod
    def pad_para(para: str, char: str = " ") -> str:
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

        lst: list[str] = []
        for i, child in enumerate(self.children):
            if i == self.num_children() // 2:
                lst.append(Node.make_branch(repr(self.value)))
            lst.append(Node.pad_para(repr(child)))
        return "\n".join(lst)


if __name__ == "__main__":
    pass
