from bfast import AST, Node
from tokenizer import TokenArgType
from .commands import Main
from for_error import CompilerExceptions
from .types import *


class CommandNotFound(CompilerExceptions):
    module = 'HighBF'
    error_line_format = 'Команда не найдена'


class VariableErrors(CompilerExceptions):
    module = 'HighBF'


class VariableAlreadyRegister(VariableErrors):
    error_line_format = 'Переменная уже зарегистрированнав пространстве имён. Используйте' \
                        ' `unvar` или измените имя.'


class VariableNotRegistered(VariableErrors):
    error_line_format = 'Переменная не объявлена в этом пространстве имён.'


class VariableTypeError(VariableErrors):
    error_line_format = 'Невозможно освободить не переменную.'


class Namespace:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent or None

    def get_child(self):
        return Namespace(self)

    def get(self, key, default=None, search_everywhere=True):
        if search_everywhere:
            try:
                return self[key]
            except KeyError:
                return default
        else:
            try:
                return self.symbols[key]
            except KeyError:
                return default

    def __contains__(self, item):
        if self.parent is None:
            return item in self.symbols
        else:
            if item in self.symbols:
                return True
            else:
                return item in self.parent

    def contain_this(self, item):
        return item in self.symbols

    def pop(self, key, default=None):
        self.symbols.pop(key, default)

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
    def __init__(self):
        self.code = []
        self.registers = set()
        self.MP = 0
        self.namespaces = []
        namespace = Namespace()
        namespace["__main"] = Macro(Main)
        self.namespaces.append(namespace)

    @property
    def namespace(self):
        return self.namespaces[-1]

    def register_name(self):
        pass

    def register_var(self, name):
        if name in self.namespace:
            raise VariableAlreadyRegister(None)

        i = 0
        while i in self.registers:
            i += 1

        self.registers.add(i)

        self.namespace[name] = Register(i, name)

    def unregister_var(self, name):
        item = self.namespace.get(name, search_everywhere=False)

        if item is None:
            raise VariableNotRegistered(None)

        if isinstance(item, Register):
            self.registers.remove(item.addr)
            self.namespace.pop(name)
        else:
            raise VariableTypeError(None)

    def new_block(self):
        namespace = Namespace(self.namespace)
        self.namespaces.append(namespace)

    def close_block(self):
        del self.namespaces[-1]

    def type_converter(self, arg):
        arg_type, value = arg

        if TokenArgType.Number == arg_type:
            return Int(value)
        else:
            try:
                return self.namespace[value]
            except KeyError:
                return UnknownName(value)

    def compile(self, node: Node):
        cmd = self.namespace[node.token.cmd]

        if isinstance(cmd, Macro):
            cmd = cmd.cmd(self)
            args = [self.type_converter(arg) for arg in node.token.args]
            try:
                # Если вдруг при обработке выкинется это сообщение
                return cmd.compile(args, node)
            except VariableErrors as e:
                e.token = node.token
                raise e
        else:
            raise CommandNotFound(node.token)
