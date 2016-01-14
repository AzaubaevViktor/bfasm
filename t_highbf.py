from bfast import AST
from compilers import HighBF
from compilers.bf import BFCompiler
from tokenizer import Tokenizer

prg = """
__plus 1
__print

var test

__minus 2
__print

__gomps 1
__plus 3
__cycle
    __read
    __minus 1
    __cycle
        __print
        __plus -1
    __plus 3
    __minus 3
"""

line = "=============================="

tokens = Tokenizer(prg.split("\n"))
tokens.parse()
print(tokens.tokens)
print(line)

ast = AST(tokens)
ast.generate()
print(ast.root)
print(line)

compiler = HighBF()

code = compiler.compile(ast.root)
print(code)
print(line)

bf_compiler = BFCompiler()
bf_compiler += code

print(bf_compiler.code)

