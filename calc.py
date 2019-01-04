import operator


class Token:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'Token({self.__class__.__name__}, {repr(self.value)})'

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.value == other.value


class Integer(Token):
    def __init__(self, value):
        super().__init__(int(value))


class Operator(Token):
    pass


class Lparen(Token):
    def __init__(self):
        super().__init__('(')


class Rparen(Token):
    def __init__(self):
        super().__init__(')')


class Lexer:
    OPERATORS = '+-*/^'

    def __init__(self, text):
        self.text = text
        self.pos = 0

    def __bool__(self):
        return self.pos < len(self.text)

    def __iter__(self):
        return self

    def __next__(self):
        self.spaces()
        if self:
            if self.char().isdigit():
                return self.integer()
            if self.char() in Lexer.OPERATORS:
                return self.operator()
            if self.char() == '(':
                return self.lparen()
            if self.char() == ')':
                return self.rparen()
            self.error()
        else:
            raise StopIteration()

    def error(self):
        raise Exception(
            f'Unrecognized character at position {self.pos} : {self.char()}'
        )

    def char(self):
        return self.text[self.pos]

    def advance(self):
        self.pos += 1

    def read(self, cond=lambda x: True):
        characters = ''
        while self and cond():
            characters += self.char()
            self.advance()
        return characters

    def spaces(self):
        self.read(lambda: self.char().isspace())

    def integer(self):
        return Integer(self.read(lambda: self.char().isdigit()))

    def operator(self):
        char = self.char()
        self.advance()
        return Operator(char)

    def lparen(self):
        self.advance()
        return Lparen()

    def rparen(self):
        self.advance()
        return Rparen()


class Precedence:
    ADDSUB, MULDIV, EXP, FACTOR = range(4)
    MIN = ADDSUB
    MAX = FACTOR


class Interpreter:
    precedences = {
        '+': Precedence.ADDSUB,
        '-': Precedence.ADDSUB,
        '*': Precedence.MULDIV,
        '/': Precedence.MULDIV,
        '^': Precedence.EXP
    }

    symbol = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.floordiv,
        '^': operator.pow
    }

    def __init__(self, text):
        self.tokens = Lexer(text)
        self.advance()

    def advance(self):
        try:
            self.token = next(self.tokens)
        except StopIteration:
            self.token = None

    def error(self, token_type):
        raise Exception(
            f'Error parsing input: expecting token of type "{token_type}", but got value "{self.token}"'
        )

    def eat(self, token_type):
        if isinstance(self.token, token_type):
            token = self.token
            self.advance()
            return token
        else:
            self.error(token_type)

    def eat_parens(self):
        self.eat(Lparen)
        result = self.expr()
        self.eat(Rparen)
        return result

    def factor(self):
        if self.token and isinstance(self.token, Integer):
            return self.eat(Integer).value
        else:
            return self.eat_parens()

    def operator(self):
        return self.eat(Operator)

    def expr(self, precedence=Precedence.MIN):
        result = self.expr(
            precedence + 1) if precedence < Precedence.MAX else self.factor()
        while self.token and self.precedence() == precedence:
            operator = self.operator()
            right = self.expr(precedence + 1)
            result = self.symbol[operator.value](result, right)
        return result

    def precedence(self):
        return Interpreter.precedences.get(self.token.value, -1)


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
