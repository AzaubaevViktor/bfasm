import copy

from ast import AST, Node
from .commands import Main, NativeSetMPS
from .types import Register, Macro
from for_error import generate_error_string


class CommandNotFound(Exception):
    def __init__(self, token):
        self.token = token

    def __str__(self):
        return generate_error_string('HighBF', 'Команда не найдена', {},
                                     (self.token.file, self.token.line_n, self.token.pos), self.token.raw)


class Namespace:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent or None

    def get_child(self):
        return Namespace(self)

    def __setitem__(self, key, value):
        self.symbols[key] = value

    def __delitem__(self, key):
        del self.symbols[key]

    def __getitem__(self, item):
        if self.parent is None:
            return self.symbols[item]
        else:
            try:
                return self.symbols[item]
            except KeyError:
                return self.parent[item]


class HighBF:
    def __init__(self, parent_namespace=None):
        self.code = []
        self.registers = set()
        self.MP = 0
        if parent_namespace:
            self.namespace = Namespace(parent_namespace)
        else:
            self.namespace = Namespace()
            self.namespace["__main"] = Macro(Main)

    def register_name(self):
        pass

    def register_var(self, name):
        pass

    def unregister_var(self, name):
        pass

    def get_child(self):
        return HighBF(self.namespace)

    def compile(self, node: Node):
        cmd = self.namespace[node.token.cmd]

        if isinstance(cmd, Macro):
            cmd = cmd.cmd(self)
            return cmd.compile(node.token.args, node)
        else:
            raise CommandNotFound(node.token)
