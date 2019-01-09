from calculator.lexer import Lexer
from calculator.lexeme import Integer, Operator, Lparen, Rparen


def test_lexer():
    text = '     2    -   (8 + 9)    *  3   /  2 ^   5'
    expected = [
        Integer(2),
        Operator('-'),
        Lparen(),
        Integer('8'),
        Operator('+'),
        Integer('9'),
        Rparen(),
        Operator('*'),
        Integer('3'),
        Operator('/'),
        Integer('2'),
        Operator('^'),
        Integer('5')
    ]
    assert list(Lexer(text)) == expected
