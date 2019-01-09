import operator

from calculator.parser import Parser


class Visitor:

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, lambda x: self.generic_visit(method_name))
        return visitor(node)

    def generic_visit(self, method_name):
        raise Exception(f'No method {method_name}')


class Interpreter(Visitor):
    symbol = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
        '^': operator.pow,
    }

    def visit_BinaryOperator(self, node):
        return Interpreter.symbol[node.op](self.visit(node.left), self.visit(node.right))

    def visit_Number(self, node):
        return node.value

    def interpret(self, text):
        return self.visit(Parser(text).parse())


class Lispy(Visitor):

    def visit_children(self, node):
        return f'{self.visit(node.left)} {self.visit(node.right)}'

    def visit_BinaryOperator(self, node):
        return f'({node.op} {self.visit_children(node)})'

    def visit_Number(self, node):
        return str(node.value)


if __name__ == '__main__':
    print(Lispy().visit(Parser('2 + 5 ^ 2 * 3').parse()))
