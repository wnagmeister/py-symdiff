from tree import Node
import pytest

# pyright: basic

@pytest.fixture
def SubClass():
    class SubNode(Node):
        pass

    return SubNode


def test_node(SubClass):
    node1 = Node.leafify(1)
    node2 = Node.leafify(2)
    node3 = SubClass(3, [node1, node2])
    assert isinstance(node3, Node)
    assert type(node3) is not Node
    assert node3.children == [node1, node2]


def test_leafify(SubClass):
    node = Node.leafify(2)
    assert node.children == []
    assert node.value == 2
    subnode = SubClass.leafify(6)
    assert subnode.children == []
    assert subnode.value == 6
    assert isinstance(subnode, Node)
    assert type(subnode) is not Node


def test_is_leaf():
    node1 = Node(3, [Node(0, [])])
    node2 = Node(5, [])
    assert not node1.is_leaf()
    assert node2.is_leaf()


@pytest.fixture
def test_tree():
    node1 = Node.leafify(1)
    node2 = Node.leafify(2)
    node3 = Node(3, [node2])
    node4 = Node(4, [node1, node3])
    node5 = Node.leafify(5)
    node6 = Node(6, [node5])
    node7 = Node(7, [node4, node6])
    return node7


def test_height(test_tree):
    assert test_tree.height() == 3
    node = Node.leafify(19)
    assert node.height() == 0


def test_is_equal():
    tree1 = Node(1, [])
    tree2 = Node(2, [])
    assert not tree1.is_equal(tree2)
    assert not tree2.is_equal(tree1)
    tree3 = Node(8, [Node.leafify(7), Node.leafify(81)])
    tree4 = Node(8, [Node.leafify(7)])
    tree5 = Node(8, [Node.leafify(7), Node.leafify(81)])
    assert not tree3.is_equal(tree4)
    assert tree3.is_equal(tree5)
    assert tree1.is_equal(tree2, lambda x, y: True)


def test_substitute(test_tree):
    node8 = Node.leafify(8)
    node4 = test_tree.children[0]
    test_tree.substitute(test_tree.children[0], node8)
    assert test_tree.children[0] is node8
    assert test_tree.children[1].value == 6
    assert node4.value == 4


def test_iter(test_tree):
    num = 0
    for i, node in enumerate(test_tree):
        assert node.value == i + 1
        num += 1
    assert num == 7
    for i, node in enumerate(test_tree):
        for i, child in enumerate(node.children):
            node.children[i] = Node(child.value * 10, child.children)
    for i, node in enumerate(test_tree):
        if node is not test_tree:
            assert node.value == 10 * (i + 1)
