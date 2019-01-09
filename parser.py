from calculator.tree import Number, BinaryOperator
from calculator.lexer import Lexer
from calculator.lexeme import Integer, Operator, Lparen, Rparen


class Precedence:
    ADDSUB, MULDIV, EXP, FACTOR = range(4)
    MIN = ADDSUB
    MAX = FACTOR


class Parser:
    precedences = {
        '+': Precedence.ADDSUB,
        '-': Precedence.ADDSUB,
        '*': Precedence.MULDIV,
        '/': Precedence.MULDIV,
        '^': Precedence.EXP,
    }

    def __init__(self, text):
        self.tokens = list(Lexer(text))
        self.position = 0

    def __bool__(self):
        return self.position < len(self.tokens)

    def current(self):
        return self.tokens[self.position]

    def precedence(self):
        return Parser.precedences.get(self.current().value, - 1)

    def advance(self):
        self.position += 1

    def read(self, token_type):
        if isinstance(self.current(), token_type):
            res = self.current().value
            self.advance()
            return res
        else:
            raise ValueError(
                f'Expected token type {token_type} but got: {self.current()}')

    def factor(self):
        if isinstance(self.current(), Integer):
            return Number(self.read(Integer))
        else:
            return self.parens()

    def op(self):
        return self.read(Operator)

    def parens(self):
        self.read(Lparen)
        result = self.expr()
        self.read(Rparen)
        return result

    def expr(self, precedence=Precedence.MIN):
        left = self.expr(precedence + 1) if precedence < Precedence.MAX else self.factor()
        while self and self.precedence() == precedence:
            op = self.op()
            right = self.expr(precedence + 1)
            left = BinaryOperator(op, left, right)
        return left

    def parse(self):
        return self.expr()


def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        print(Interpreter(text).expr())


if __name__ == '__main__':
    main()
