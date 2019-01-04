from quicktest import test
from calc import Interpreter


def interpret(text):
    return Interpreter(text).expr()


if __name__ == '__main__':
    test(
        interpret,
        [
            [
                '(2 + (7 - 4)) * 5 ^ 2 - 14 / 2',
                118
            ]
        ]
    )
