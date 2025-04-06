from .interpreter import Interpreter
from .exceptions import ExitREPL
from .lexer import Lexer
from .parser import Parser


def repl():
    print("JxLang REPL (输入 endend() 退出，输入 version() 查看版本)")
    interpreter = Interpreter()
    while True:
        text_lines = []
        prompt = "jxlang> "
        while True:
            try:
                line = input(prompt).strip().replace('\r', '')
                if not line:
                    continue
                text_lines.append(line)
                full_text = "\n".join(text_lines)
                lexer = Lexer(full_text)
                parser = Parser(lexer)
                tree = parser.parse()
                break
            except EOFError:
                prompt = "    ... "
            except Exception as e:
                print(f"Syntax Error: {e}")
                text_lines = []
                break
        if not text_lines:
            continue

        try:
            result = interpreter.visit(tree)
            if result is not None:
                print(result)
        except ExitREPL as e:
            print(f"Exiting with code {e.code}")
            break
        except Exception as e:
            print(f"Runtime Error: {e}")