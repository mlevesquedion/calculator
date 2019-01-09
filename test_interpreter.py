from calculator.interpreter import Interpreter


def test():
    expr = '(2 + (7 - 4)) * 5 ^ 2 - 14 / 2'
    expected = 118
    assert Interpreter().interpret(expr) == expected
