from ast import AST
from compilers import HighBF
from tokenizer import Tokenizer

prg = """
__plus 100
__print

__minus 10
__print

__gomps 1
__plus 1
__cycle
    __read
    __minus 1
    __print
    __minus 100
"""

tokens = Tokenizer(prg.split("\n"))
tokens.parse()
print(tokens.tokens)

ast = AST(tokens)
ast.generate()
print(ast.root)

compiler = HighBF()

code = compiler.compile(ast.root)
print(code)

