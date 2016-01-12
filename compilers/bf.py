from enum import Enum


class Cmd(Enum):
    Plus = 0
    Minus = 1
    Left = 2
    Right = 3
    Print = 4
    Read = 5
    CycleOp = 6
    CycleStop = 7
    Nop = 8

cmd_assoc = ['+', '-', '<', '>', '.', ',', '[', ']', '']


class BFCompiler:
    def __init__(self):
        self.code = ""

    def __iadd__(self, other):
        if isinstance(other, tuple):
            cmd, count = other
            if isinstance(cmd, Cmd) and isinstance(count, int):
                self.code += cmd_assoc[cmd.value] * count
            else:
                raise TypeError()
        elif isinstance(other, list):
            for cmd in other:
                self.__iadd__(cmd)
        else:
            raise TypeError()
