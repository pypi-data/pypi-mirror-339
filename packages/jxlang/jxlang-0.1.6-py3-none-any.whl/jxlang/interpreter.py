from .tokens import Token, TokenType
from .exceptions import ExitREPL
import importlib, datetime, itertools


# ---------- 解释器 (Evaluator) ----------
class Interpreter:
    def __init__(self):
        self.symbols = {}     # 符号表
        self.loop_stack = []  # 跟踪循环层级
        self.libraries = {}   # 存储已导入的库
        self.functions = {}   # 存储函数定义

    def visit_FUNC_DEF(self, node):
        # 存储函数定义
        self.functions[node['name']] = {
            'params': node['params'],
            'body': node['body']
        }
        return None

    def visit_FUNC_CALL(self, node):
        # 获取函数定义
        func = self.functions.get(node['name'])
        if not func:
            raise Exception(f"Function {node['name']} not defined")

        # 绑定参数
        params = func['params']
        args = node['args']
        if len(params) != len(args):
            raise Exception(f"Args are not match: need {len(params)}，got {len(args)}")

        # 创建新作用域
        old_symbols = self.symbols.copy()
        for param, arg in zip(params, args):
            self.symbols[param] = self.visit(arg)

        # 执行函数体
        result = None
        for stmt in func['body']:
            result = self.visit(stmt)
            if stmt['type'] == 'RETURN':
                break

        # 恢复作用域
        self.symbols = old_symbols
        return result

    def visit_RETURN(self, node):
        return self.visit(node['value'])

    def visit_VERSION_CALL(self, node):
        current_year = datetime.datetime.now().year
        return f"jxlang 0.0.1 2025-{current_year}"

    def visit_CITE(self, node):
        library_name = node['name']
        try:
            # 直接导入 Python 模块
            lib_module = importlib.import_module(library_name)
            self.libraries[library_name] = lib_module
            self.symbols[library_name] = lib_module
        except ModuleNotFoundError:
            raise Exception(f"Python library '{library_name}' not found")

    def visit_MEMBER_ACCESS(self, node):
        # 获取 Python 模块对象
        obj = self.visit(node['object'])
        member_name = node['member']
        # 获取模块中的属性或方法
        if hasattr(obj, member_name):
            return getattr(obj, member_name)
        else:
            raise Exception(f"Method '{member_name}' not found in library")

    def visit_CALL(self, node):
        # 解析函数对象
        func = self.visit(node['func'])
        # 解析参数
        args = [self.visit(arg) for arg in node['args']]
        # 调用 Python 函数并返回结果
        return func(*args)

    def visit_BIN_OP(self, node):
        left = self.visit(node['left'])
        right = self.visit(node['right'])
        op = node['op']

        if op == TokenType.PLUS:
            return left + right
        elif op == TokenType.MINUS:
            return left - right
        elif op == TokenType.MUL:
            return left * right
        elif op == TokenType.DIV:
            return left / right  # 注意除零错误
        elif op == TokenType.MOD:
            return left % right
        else:
            raise Exception("Unknown operator")

    # 处理列表求值
    def visit_LIST(self, node):
        return [self.visit(elem) for elem in node['value']]

    # 处理布尔值
    def visit_BOOL(self, node):
        return node['value']

    # 处理浮点数
    def visit_FLOAT(self, node):
        return node['value']

    # 处理字符串
    def visit_STRING(self, node):
        return node['value']

    def visit(self, node):
        method_name = f'visit_{node["type"]}'
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        raise Exception(f"No visit_{node['type']} method")

    def visit_LET(self, node):
        for var_name, value_node in node['vars']:
            value = self.visit(value_node)
            self.symbols[var_name] = value
        return None

    def visit_FOR_LOOP(self, node):
        variables = node['vars']
        start = self.visit(node['start'])
        end = self.visit(node['end'])
        body = node['body']

        # 生成循环范围
        ranges = [range(start, end + 1)] * len(variables)

        # 遍历所有变量组合
        for values in itertools.product(*ranges):
            # 新建作用域
            self.loop_stack.append(self.symbols.copy())

            # 绑定变量到当前作用域
            for var, val in zip(variables, values):
                self.symbols[var] = val

            # 执行循环体
            self.visit(body)

            # 恢复上一层作用域
            self.symbols = self.loop_stack.pop()

        return None

    def visit_TABLE(self, node):
        return [self.visit(sublist) for sublist in node['value']]

    def visit_INT(self, node):
        return node['value']

    def visit_VAR(self, node):
        var_name = node['value']
        if var_name in self.symbols:
            return self.symbols[var_name]
        else:
            raise Exception(f"Undefined variable {var_name}")

    # 处理 enter()
    def visit_ENTER_CALL(self, node):
        user_input = input()
        try:
            return int(user_input)  # 尝试转为整数
        except ValueError:
            try:
                return float(user_input)  # 尝试转为浮点数
            except ValueError:
                return user_input  # 保留为字符串

    # 处理 say(expr)
    def visit_SAY(self, node):
        value = self.visit(node['expr'])
        print(value)
        return None

    # 处理 endend()
    def visit_ENDEND(self, node):
        arg = node.get('arg')
        if arg is not None:
            if not (0 <= arg <= 9):  # 检查参数范围
                raise Exception("endend() argument must be between 0 and 9")
            raise ExitREPL(arg)
        else:
            raise ExitREPL(0)  # 默认退出码为 0