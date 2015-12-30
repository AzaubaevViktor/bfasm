from enum import Enum

from .abstract_compiler import Compiler


class Cmd(Enum):
    Plus = 0
    Minus = 1
    Left = 2
    Right = 3
    Print = 4
    Read = 5
    CycleOp = 6
    CycleStop = 7


class BFCompiler(Compiler):
    pass
