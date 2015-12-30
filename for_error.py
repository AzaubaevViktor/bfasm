

def generate_error_string(module: str,
                          error_line_format: str,
                          kwargs: dict,
                          pos: tuple,
                          raw_str: str):
    module = module.rstrip().lstrip()

    underline = ""
    pos_cur = 0
    words = []
    for word in raw_str.split(" "):
        if '' == word:
            words.append(" ")
        else:
            words += [word, " "]

    for word in words:
        if pos_cur <= pos[2] < pos_cur + len(word):
            underline += "^" * len(word)
            break
        else:
            underline += " " * len(word)
            pos_cur += len(word)

    s = "Ошибка в модуле `{}`\n".format(module) + \
        error_line_format.format(**kwargs) + "\n"\
        "on '{0}':{1}:{2}:\n".format(*pos) + \
        raw_str + "\n" + \
        underline
    return s


if __name__ == "__main__":
    _ = generate_error_string('Test', 'line{b}{a}', {'a': '1', 'b': '2'}, ('file.abf', 1, 9), '     aaad 1 22 333')
    print(_)