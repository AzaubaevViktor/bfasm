class HighBFObject:
    pass


class TokenType(HighBFObject):
    pass


class Int(HighBFObject):
    pass


class Macro(HighBFObject):
    def __init__(self, cmd):
        self.cmd = cmd

    def __repr__(self):
        return "<Macro/{}>".format(self.cmd)


class Register(HighBFObject):
    def __init__(self, addr):
        self.addr = addr

    def __repr__(self):
        return "<Reg#{}>".format(self.addr)



class StackPointer(HighBFObject):
    pass