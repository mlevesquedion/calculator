class AST:
    pass


class BinaryOperator(AST):

    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class Number(AST):

    def __init__(self, value):
        self.value = value
