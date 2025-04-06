from .interpreter import Interpreter
from .exceptions import ExitREPL
from .lexer import Lexer
from .parser import Parser


def repl():
    print("JxLang REPL (输入endend()退出,输入version()查看当前版本)")
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