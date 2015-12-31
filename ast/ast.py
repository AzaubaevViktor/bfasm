from for_error import generate_error_string
from tokenizer import Token


class Branch:
    def __init__(self, parent, value: Token):
        self.parent = parent
        self.value = value
        self.level = value.level
        self.childs = []

        if parent is not None:
            parent.append(self)

    def append(self, child):
        self.childs.append(child)

    def __repr__(self):
        level = "* " * self.level
        s = level + "{}\n".format(self.value)

        for child in self.childs:
            s += "{}".format(child)

        return s


class LevelSequenceError(Exception):
    def __init__(self, token):
        self.token = token

    def __str__(self):
        return generate_error_string('AST', 'Последовательность уровней не соблюдена', {},
                                     (self.token.file, self.token.line_n, self.token.pos), self.token.raw)


class AST:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.ast = None

    def generate(self):
        init_token = Token('__init', -1, [])
        ast = Branch(None, init_token)
        self.ast = ast

        for token in self.tokenizer.tokens:
            if token.level == ast.level + 1:
                branch = Branch(ast, token)
                ast = branch

            elif token.level == ast.level:
                ast = Branch(ast.parent, token)

            elif token.level < ast.level:
                while token.level < ast.level:
                    ast = ast.parent
                ast = Branch(ast.parent, token)
            else:
                raise LevelSequenceError(token)