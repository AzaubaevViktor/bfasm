from .bf import Cmd


class BF1Compiler:
    def __init__(self, start_cell=0):
        self.code = []
        self.cur_cell = start_cell
        self.start_cell = start_cell

    def _add(self, cmd: Cmd, count: int):
        self.code.append((cmd, count))

    def _append(self, bf1):
        if isinstance(bf1, BF1Compiler):
            self.move(bf1.start_cell)
            self.code += bf1.code
            self.cur_cell = bf1.cur_cell

    def move(self, cell: int):
        """Сдвигает указатель текущей ячейки"""
        rel = cell - self.cur_cell
        if rel > 0:
            self._add(Cmd.Right, rel)
        elif rel < 0:
            self._add(Cmd.Left, -rel)
        self.cur_cell = cell

    def null(self, cell):
        bf1 = BF1Compiler(cell)
        bf1._add(Cmd.Minus, 1)
        self.cycle(cell, bf1)

    def plus(self, cell, value):
        self.move(cell)
        if value > 0:
            self._add(Cmd.Plus, value)
        elif value < 0:
            self._add(Cmd.Minus, -value)

    def print(self, cell):
        self.move(cell)
        self._add(Cmd.Print, 1)

    def read(self, cell):
        self.move(cell)
        self._add(Cmd.Read, 1)

    def cycle(self, cell_cond, bf1compiler):
        self.move(cell_cond)
        self._add(Cmd.CycleOp, 1)
        self._append(bf1compiler)
        self.move(cell_cond)
        self._add(Cmd.CycleStop, 1)

    def a_mov_add_b(self, acell, bcell):
        """
        b += a
        a = 0
        """
        bf1 = BF1Compiler(acell)
        bf1.plus(acell, -1)
        bf1.plus(bcell, 1)

        self.cycle(acell, bf1)

    def a_mov_b(self, acell, bcell):
        """
        b = a
        a = 0
        """
        self.null(bcell)
        self.a_mov_add_b(acell, bcell)

    def a_copy_b(self, acell, bcell, tcell):
        """
        b = a
        t = 0
        """
        self.null(tcell)
        self.null(bcell)

        bf1 = BF1Compiler(acell)
        bf1.plus(acell, -1)
        bf1.plus(bcell, 1)
        bf1.plus(tcell, 1)

        self.cycle(acell, bf1)

        self.a_mov_b(tcell, acell)

    def ifelse(self, cell_cond, tcell, true_bf, false_bf):
        """
        true_bf и false_bf должны начинаться с acell
        if cell_cond:
            true_bf
        else:
            false_bf
        t = 0
        """
        # True
        true_bf.null(tcell)
        true_bf.null(cell_cond)

        # False
        _false_bf = BF1Compiler(tcell)
        _false_bf.move(cell_cond)
        _false_bf._append(false_bf)
        _false_bf.null(tcell)
        _false_bf.move(tcell)

        self.null(tcell)
        self.plus(tcell, 1)
        self.cycle(cell_cond, true_bf)
        self.cycle(tcell, _false_bf)
