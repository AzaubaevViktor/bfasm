class HighBFObject:
    pass


class TokenType(HighBFObject):
    pass


class Int(HighBFObject):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "<Int/{}>".format(self.value)

    def __neg__(self):
        return Int(-self.value)


class Macro(HighBFObject):
    def __init__(self, cmd):
        self.cmd = cmd

    def __repr__(self):
        return "<Macro/{}>".format(self.cmd)


class Register(HighBFObject):
    def __init__(self, addr, name):
        self.addr = addr
        self.name = name

    def __repr__(self):
        return "<Reg_`{}`#{}>".format(self.name, self.addr)


class StackPointer(HighBFObject):
    pass


class UnknownName(HighBFObject):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<UnkName/{}>".format(self.name)
