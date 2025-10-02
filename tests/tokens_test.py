from tokens import tokenify, string_to_tokens, shunting_yard
from symbols import Variable, Operator, operators
from astree import AstNode
import pytest

string_expressions = [
    (
        "3 * ( x + 2 ) - sin ( y )",
        [
            3.0,
            Variable("x"),
            2.0,
            operators["+"],
            operators["*"],
            Variable("y"),
            operators["sin"],
            operators["-"],
        ],
        AstNode(
            operators["-"],
            [
                AstNode(
                    operators["*"],
                    [
                        AstNode.leafify(3.0),
                        AstNode(
                            operators["+"],
                            [AstNode.leafify(Variable("x")), AstNode.leafify(2)],
                        ),
                    ],
                ),
                AstNode(operators["sin"], [AstNode.leafify(Variable("y"))]),
            ],
        ),
    ),
    (
        "1.5 / ( b + exp ( constantpi ) )",
        [
            1.5,
            Variable("b"),
            Variable("constantpi"),
            operators["exp"],
            operators["+"],
            operators["/"],
        ],
        AstNode(
            operators["/"],
            [
                AstNode.leafify(1.5),
                AstNode(
                    operators["+"],
                    [
                        AstNode.leafify(Variable("b")),
                        AstNode(
                            operators["exp"], [AstNode.leafify(Variable("constantpi"))]
                        ),
                    ],
                ),
            ],
        ),
    ),
    (
        "ln x + -7.8 * x",
        [
            Variable("x"),
            operators["ln"],
            -7.8,
            Variable("x"),
            operators["*"],
            operators["+"],
        ],
        AstNode(
            operators["+"],
            [
                AstNode(operators["ln"], [AstNode.leafify(Variable("x"))]),
                AstNode(
                    operators["*"],
                    [AstNode.leafify(-7.8), AstNode.leafify(Variable("x"))],
                ),
            ],
        ),
    ),
]


def test_tokenify():
    assert isinstance(tokenify("x"), Variable)
    assert isinstance(tokenify("*"), Operator)
    assert isinstance(tokenify("3.14"), float)
    assert isinstance(tokenify("-19.4"), float)
    assert isinstance(tokenify("12rubbish"), Variable)
    assert isinstance(tokenify("1-2"), Variable)


@pytest.mark.parametrize("infix_string, rpn_tokens, asttree", string_expressions)
def test_shunting_yard(infix_string, rpn_tokens, asttree):
    assert shunting_yard(string_to_tokens(infix_string)) == rpn_tokens
