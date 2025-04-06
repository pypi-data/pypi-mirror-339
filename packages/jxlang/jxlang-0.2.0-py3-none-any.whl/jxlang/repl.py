from .interpreter import Interpreter
from .exceptions import ExitREPL
from .lexer import Lexer
from .parser import Parser

# ---------- REPL 交互式环境 ----------
def repl():
    interpreter = Interpreter()
    while True:
        try:
            text = input("jxlang> ")
            lexer = Lexer(text)
            parser = Parser(lexer)
            tree = parser.parse()
            result = interpreter.visit(tree)
            if result is not None:
                print(result)
        except ExitREPL as e:
            print(f"Exiting with code {e.code}")
            break
        except Exception as e:
            print(f"Error: {e}")