from abc import abstractmethod

from .types import Register, Macro, Int
# from .highbf import HighBF
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
    arg_types = []

    def __init__(self, compiler):
        self.compiler = compiler

    def _argument_checker(self, args):
        if len(args) != len(self.arg_types):
            raise ArgumentError(None, None, "Несовпадает количество аргументов")

        for arg_type, arg in zip(self.arg_types, args):
            if not isinstance(arg[0], arg_type):
                raise ArgumentError(arg, arg_type, "Несовпадение типов")

    def compile(self, args, block):
        # self._argument_checker(args)
        return self._compile(args, block)

    @abstractmethod
    def _compile(self, args, block):
        pass


class Main(AbstractCommand):
    def _compile(self, args, block):
        std_namespace = {
            "N0": Register(0),
            "N1": Register(1),
            "SR1": Register(2),
            "X": Register(3),
            "Y": Register(4),
            "SR2": Register(5),
            "A": Register(6),
            # flasgs
            "L": Register(7),
            "S": Register(8),
            "__setmps": Macro(NativeSetMPS),
            "__gomp": Macro(NativeGoMP),
            "__gomps": Macro(NativeGoMPS),
            "__at": Macro(NativeAt),
            "__ats": Macro(NativeAtS),
            "__plus": Macro(NativePlus),
            "__minus": Macro(NativeMinus),
            "__cycle": Macro(NativeCycle),
            "__print": Macro(NativePrint),
            "__read": Macro(NativeRead)
        }
        for k, v in std_namespace.items():
            self.compiler.namespace[k] = v

        code = []

        for children in block.childs:
            code += self.compiler.compile(children)
        return code


class NativeSetMPS(AbstractCommand):
    arg_types = [Int]

    def _compile(self, args, block):
        self.compiler.MP = args[0][1]
        return [(Cmd.Nop, 0)]


def _move(to, fr):
    if to > fr:
        return [(Cmd.Right, to - fr)]
    else:
        return [(Cmd.Left, fr - to)]


def _plus(n):
    if n > 0:
        return [(Cmd.Plus, n)]
    else:
        return [(Cmd.Minus, -n)]


class NativeGoMP(AbstractCommand):
    arg_types = [Register]

    def _compile(self, args, block):
        MP = self.compiler.MP
        self.compiler.MP = args[0][1]
        return _move(args[0][1], MP)


class NativeGoMPS(NativeGoMP):
    arg_types = [Int]


class NativeAt(AbstractCommand):
    arg_types = [Register, Register]

    def _compile(self, args, block):
        r1 = args[0][1]
        r2 = args[1][1]

        self.compiler.MP = r2 - r1
        return _move(r2, r1)


class NativeAtS(AbstractCommand):
    arg_types = [Int]

    def _compile(self, args, block):
        d = args[0][1]
        self.compiler.MP += d
        return _move(d, 0)


class NativePlus(AbstractCommand):
    arg_types = [Int]

    def _compile(self, args, block):
        return _plus(args[0][1])


class NativeMinus(AbstractCommand):
    arg_types = [Int]

    def _compile(self, args, block):
        return _plus(-args[0][1])


class NativeCycle(AbstractCommand):
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