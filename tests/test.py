from tree import Node
from astree import AstNode
from rules import apply_all_rules


def shunting_yard_test():
    pass


def tree_test():
    one = Node.leafify(1)
    two = Node.leafify(2)
    three = Node.join(3, [two])
    four = Node.join(4, [one, three])
    five = Node.leafify(5)
    six = Node.join(6, [five])
    seven = Node.join(7, [four, six])

    print(seven)
    assert five.is_leaf()
    assert not three.is_leaf()


def astify_test():
    pass


def rule_test():
    pass


if __name__ == "__main__":
    tree_test()
