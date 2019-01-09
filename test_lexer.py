from quicktest import test
from lexer import Lexer
from token import Integer, Operator, Lparen, Rparen


def lex(text):
    return list(Lexer(text))


if __name__ == '__main__':
    test(
        lex,
        [
            [
                '     2    -   (8 + 9)    *  3   /  2 ^   5',
                [
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
            ]
        ]
    )
