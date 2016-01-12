from for_error import generate_error_string
from tokenizer import Token


class Node:
    def __init__(self, parent, token: Token):
        self.parent = parent
        self.token = token
        self.level = token.level
        self.childs = []

        if parent is not None:
            parent.append(self)

    def append(self, child):
        self.childs.append(child)

    def __repr__(self):
        level = "* " * self.level
        s = level + "{}\n".format(self.token)

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
        self.root = None

    def generate(self):
        init_token = Token('__main', -1, [])
        node = Node(None, init_token)
        self.root = node

        for token in self.tokenizer.tokens:
            if token.level == node.level + 1:
                branch = Node(node, token)
                node = branch

            elif token.level == node.level:
                node = Node(node.parent, token)

            elif token.level < node.level:
                while token.level < node.level:
                    node = node.parent
                node = Node(node.parent, token)
            else:
                raise LevelSequenceError(token)