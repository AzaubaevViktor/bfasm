from abc import abstractmethod, ABC


class Compiler(ABC):
    def __init__(self, child):
        self.child = child

    @abstractmethod
    def compile(self):
        pass
