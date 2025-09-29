from symbols import *
from tokens import *
from tree import Node
from astree import AstNode
from rules import apply_all_rules


def shunting_yard_test():
    string1 = "1 + exp y oq2"
    tokens = string_to_tokens(string1)
    assert isinstance(tokens[0], float)
    assert tokens[1] == operators.get("+")
    assert tokens[2] == operators.get("exp")
    assert isinstance(tokens[3], Variable)
    assert isinstance(tokens[4], Variable)


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
    shunting_yard_test()
    tree_test()
