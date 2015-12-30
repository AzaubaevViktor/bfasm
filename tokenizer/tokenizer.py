from enum import Enum

from for_error import generate_error_string


class LeverError(Exception):
    def __init__(self, file, line_n,  pos, raw):
        self.file = file
        self.raw = raw
        self.pos = pos
        self.line_n = line_n

    def __str__(self):
        return generate_error_string('Tokenizer', "Количество пробелов не кратно 4м", {},
                                     (self.file, self.line_n, self.pos), self.raw)


class TokenArgType(Enum):
    Number = 0
    String = 1
    Unknown = 2


class Token:
    def __init__(self,
                 token, level, *args,
                 file=None,
                 line_n=None,
                 pos=None,
                 raw=""):
        self.token = token
        self.level = level
        self.args = []
        self._parse_args(args)
        self.file = file
        self.line_n = line_n
        self.pos = pos
        self.raw = raw

    def _parse_args(self, args: tuple):
        """
        Парсит аргументы. Умеет вычленять числа и строки, обёрнутые в одинарные кавычки `'`,
        всё остальное считает неизвестным
        :param args: tuple string
        :return:
        """
        for arg in args[0]:
            if not arg:
                continue

            try:
                int(arg)
                self.args.append((TokenArgType.Number, int(arg)))
            except ValueError:
                if 2 == arg.count("'") and arg.index("'") == 0 and arg.index("'", 1) + 1 == len(arg):
                    self.args.append((TokenArgType.String, arg[1:-1]))
                else:
                    self.args.append((TokenArgType.Unknown, arg))

    def __repr__(self):
        return "{file}:{line}:{pos} `{token}` `{args}`".format(
            file=self.file,
            line=self.line_n,
            pos=self.pos,
            token=self.token,
            args=self.args
        )


class Tokenizer:
    def __init__(self, lines):
        self.lines = lines
        self.tokens = []

    def parse(self):
        line_counter = 0
        for line in self.lines:
            line_counter += 1

            try:
                token = self._parse_line(line)
            except LeverError as e:
                e.line_n = line_counter
                raise e

            if token is not None:
                self.tokens.append(token)

    def _parse_line(self, line: str):
        level = len(line) - len(line.lstrip())
        if level % 4:
            raise LeverError(None, None, level - 1, line)
        else:
            level //= 4

        words = line.rstrip().lstrip().split(" ")
        words = [x for x in words if x]
        if 0 == len(words):
            return None

        token = words[0]
        args = words[1:]

        return Token(token, level, args,
                     pos=level * 4,
                     raw=line)


if __name__ == "__main__":
    text = """

hello

    lolka
    123 1 2 3

        test `1` 2 'string' -1234 44.44
                        wtf



        """

    tokens = Tokenizer(text.split("\n"))
    tokens.parse()
    print(tokens.tokens)

    text = "       xx"

    tokens = Tokenizer(text.split("\n"))
    tokens.parse()
    print(tokens.tokens)
