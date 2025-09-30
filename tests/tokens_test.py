from tokens import tokenify, string_to_tokens, shunting_yard
from symbols import Variable, Operator, operators


def test_tokenify():
    assert isinstance(tokenify("x"), Variable)
    assert isinstance(tokenify("*"), Operator)
    assert isinstance(tokenify("3.14"), float)
    assert isinstance(tokenify("-19.4"), float)
    assert isinstance(tokenify("12rubbish"), Variable)
    assert isinstance(tokenify("1-2"), Variable)


def test_shunting_yard():
    string1 = "1 + exp y oq2"
    tokens = string_to_tokens(string1)
    assert isinstance(tokens[0], float)
    assert tokens[1] == operators["+"]
    assert tokens[2] == operators["exp"]
    assert isinstance(tokens[3], Variable)
    assert isinstance(tokens[4], Variable)
