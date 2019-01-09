from calculator.lexeme import Integer, Operator, Lparen, Rparen


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
