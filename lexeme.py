class Lexeme:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'Token({self.__class__.__name__}, {repr(self.value)})'

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.value == other.value


class Integer(Lexeme):
    def __init__(self, value):
        super().__init__(int(value))


class Operator(Lexeme):
    pass


class Lparen(Lexeme):
    def __init__(self):
        super().__init__('(')


class Rparen(Lexeme):
    def __init__(self):
        super().__init__(')')
