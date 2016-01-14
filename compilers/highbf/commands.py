from abc import abstractmethod

from .types import *
from ..bf import Cmd


class ArgumentError(Exception):
    def __init__(self, argument, argtype, message):
        self.argtype = argtype
        self.message = message
        self.argument = argument

    def __str__(self):
        return "Ошибка в аргументе {}\n" \
               "Заявлен тип {}, необходим {}\n" \
               "{}".format(self.argument,
                           self.argument.__class__, self.argtype,
                           self.message)


class AbstractCommand:
    # Команда обязательно должна хоть что-нибудь возвращать!
    arg_types = []
    block_command = False

    def __init__(self, compiler):
        self.compiler = compiler

    def _argument_checker(self, args):
        if len(args) != len(self.arg_types):
            raise ArgumentError(None, None, "Несовпадает количество аргументов")

        for arg_type, arg in zip(self.arg_types, args):
            if not isinstance(arg, arg_type):
                raise ArgumentError(arg, arg_type, "Несовпадение типов")

    def compile(self, args, block):
        self._argument_checker(args)
        if self.block_command:
            self.compiler.new_block()
        data = self._compile(args, block)
        if self.block_command:
            self.compiler.close_block()
        return data

    @abstractmethod
    def _compile(self, args, block):
        pass


class Main(AbstractCommand):
    def _compile(self, args, block):
        std_namespace = {
            "__setmps": Macro(NativeSetMPS),
            "__gomp": Macro(NativeGoMP),
            "__gomps": Macro(NativeGoMPS),
            "__at": Macro(NativeAt),
            "__ats": Macro(NativeAtS),
            "__plus": Macro(NativePlus),
            "__minus": Macro(NativeMinus),
            "__cycle": Macro(NativeCycle),
            "__print": Macro(NativePrint),
            "__read": Macro(NativeRead),
            "var": Macro(NativeVar),
            "unvar": Macro(NativeUnVar)
        }
        for k, v in std_namespace.items():
            self.compiler.namespace[k] = v

        self.compiler.register_var("N0")
        self.compiler.register_var("N1")
        self.compiler.register_var("SR1")
        self.compiler.register_var("X")
        self.compiler.register_var("Y")
        self.compiler.register_var("SR2")
        self.compiler.register_var("A")
        self.compiler.register_var("L")
        self.compiler.register_var("S")

        # Добавить сюда флаги

        code = [(Cmd.Right, 1), (Cmd.Plus, 1), (Cmd.Left, 1)] # для N1
        # Казалось бы, зачем? Ведь можно поменять внутрикомпиляторное значение MP.
        # Но если мы так сделаем, то могут быть ошибки, если писать на PureBrainfuck

        for children in block.childs:
            code += self.compiler.compile(children)
        return code


class NativeSetMPS(AbstractCommand):
    arg_types = [Int]

    def _compile(self, args, block):
        self.compiler.MP = args[0]
        return [(Cmd.Nop, 0)]


def _move(to, fr):
    if isinstance(to, Int):
        to = to.value
    if isinstance(fr, Int):
        fr = fr.value

    if to > fr:
        return [(Cmd.Right, to - fr)]
    else:
        return [(Cmd.Left, fr - to)]


def _plus(n: Int):
    if n.value > 0:
        return [(Cmd.Plus, n.value)]
    else:
        return [(Cmd.Minus, -n.value)]


class NativeGoMP(AbstractCommand):
    arg_types = [Register]

    def _compile(self, args, block):
        MP = self.compiler.MP
        self.compiler.MP = args[0]
        return _move(args[0], MP)


class NativeGoMPS(NativeGoMP):
    arg_types = [Int]


class NativeAt(AbstractCommand):
    arg_types = [Register, Register]

    def _compile(self, args, block):
        r1 = args[0]
        r2 = args[1][1]

        self.compiler.MP = r2 - r1
        return _move(r2, r1)


class NativeAtS(AbstractCommand):
    arg_types = [Int]

    def _compile(self, args, block):
        d = args[0]
        self.compiler.MP += d
        return _move(d, 0)


class NativePlus(AbstractCommand):
    arg_types = [Int]

    def _compile(self, args, block):
        return _plus(args[0])


class NativeMinus(AbstractCommand):
    arg_types = [Int]

    def _compile(self, args, block):
        return _plus(-args[0])


class NativeCycle(AbstractCommand):
    block_command = True

    def _compile(self, args, block):
        code = [(Cmd.CycleOp, 1)]

        for children in block.childs:
            code += self.compiler.compile(children)

        code += [(Cmd.CycleStop, 1)]

        return code


class NativePrint(AbstractCommand):
    def _compile(self, args, block):
        return [(Cmd.Print, 1)]


class NativeRead(AbstractCommand):
    def _compile(self, args, block):
        return [(Cmd.Read, 1)]


class NativeVar(AbstractCommand):
    arg_types = [UnknownName]

    def _compile(self, args, block):
        self.compiler.register_var(args[0].name)
        return [(Cmd.Nop, 0)]


class NativeUnVar(AbstractCommand):
    arg_types = [Register]

    def _compile(self, args, block):
        self.compiler.unregister_var(args[0].name)
        return [(Cmd.Nop, 0)]
