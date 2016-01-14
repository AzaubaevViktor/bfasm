from bfast import AST
from tokenizer import Tokenizer

if __name__ == "__main__":
    text = """

hello

    lolka
    123 1 2 3

        test `1` 2 'string' -1234 44.44
            wtf '2123'
hey
    bababa 12
    lol
    piu1
        piu2
            piu3

                piu4
                    piu5
        pui21
            pui32

        """

    tokens = Tokenizer(text.split("\n"))
    tokens.parse()
    print(tokens.tokens)

    ast = AST(tokens)
    ast.generate()
    print(ast.root)
