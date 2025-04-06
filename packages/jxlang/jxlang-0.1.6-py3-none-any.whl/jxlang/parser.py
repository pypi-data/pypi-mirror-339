from .tokens import TokenType

# ---------- 语法分析器 (Parser) ----------
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def cite_statement(self):
        self.eat(TokenType.CITE)
        library_name = self.current_token.value
        self.eat(TokenType.ID)
        return {'type': 'CITE', 'name': library_name}

    def term(self):
        node = self.factor()
        while self.current_token.type in (TokenType.MUL, TokenType.DIV, TokenType.MOD):
            op = self.current_token.type
            self.eat(op)
            node = {
                'type': 'BIN_OP',
                'op': op,
                'left': node,
                'right': self.factor()
            }
        return node

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise Exception(f"Expected {token_type}, got {self.current_token.type}")

    def primary(self):
        token = self.current_token
        if token.type == TokenType.ID and token.value == "enter":
            # 解析 enter() 为函数调用
            return self.enter_expression()
        # 处理整数
        elif token.type == TokenType.INT:
            self.eat(TokenType.INT)
            return {'type': 'INT', 'value': token.value}
        # 处理浮点数
        elif token.type == TokenType.FLOAT:
            self.eat(TokenType.FLOAT)
            return {'type': 'FLOAT', 'value': token.value}
        # 处理字符串
        elif token.type == TokenType.STRING:
            self.eat(TokenType.STRING)
            return {'type': 'STRING', 'value': token.value}
        # 处理布尔值
        elif token.type in (TokenType.TRUE, TokenType.FALSE):
            value = token.value
            self.eat(token.type)
            return {'type': 'BOOL', 'value': value}
        # 处理变量名
        elif token.type == TokenType.ID:
            var_name = token.value
            self.eat(TokenType.ID)
            return {'type': 'VAR', 'value': var_name}
        # 处理括号表达式：( ... )
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()  # 递归解析表达式
            self.eat(TokenType.RPAREN)
            return node
        # 处理列表字面量：[ ... ]
        elif token.type == TokenType.LBRACKET:
            return self.list_expr()
        # 处理 version()
        elif token.type == TokenType.VERSION:
            return self.version_call()
        else:
            raise Exception(f"Unexpected token: {token.type}")

    def factor(self):
        node = self.primary()  # 解析基础因子（变量、数字等）
        # 处理成员访问
        while self.current_token.type == TokenType.DOT:
            self.eat(TokenType.DOT)
            member = self.current_token.value
            self.eat(TokenType.ID)
            node = {
                'type': 'MEMBER_ACCESS',
                'object': node,
                'member': member
            }
        # 处理函数调用
        if self.current_token.type == TokenType.LPAREN:
            node = self.call(node)  # 进入函数调用解析
        return node

    def version_call(self):
        """解析 version() 函数调用"""
        self.eat(TokenType.VERSION)  # 消费 'version'
        self.eat(TokenType.LPAREN)  # 消费 '('
        self.eat(TokenType.RPAREN)  # 消费 ')'
        return {'type': 'VERSION_CALL'}

    def call(self, node):
        self.eat(TokenType.LPAREN)  # 消费 '('
        args = []
        if self.current_token.type != TokenType.RPAREN:
            args.append(self.expr())  # 解析第一个参数
            while self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)  # 消费 ','
                args.append(self.expr())  # 解析后续参数
        self.eat(TokenType.RPAREN)  # 消费 ')'
        return {
            'type': 'CALL',
            'func': node,
            'args': args
        }

    def parse(self):
        return self.statement()

    def statement(self):
        if self.current_token.type == TokenType.LET:
            return self.let_statement()
        elif self.current_token.type == TokenType.LPAREN:
            return self.loop_statement()
        elif self.current_token.type == TokenType.PRINT:
            return self.print_statement()
        elif self.current_token.type == TokenType.SAY:
            return self.say_statement()
        elif self.current_token.type == TokenType.ENDEND:
            return self.endend_statement()
        elif self.current_token.type == TokenType.ENTER:
            return self.enter_expression()
        elif self.current_token.type == TokenType.CITE:
            return self.cite_statement()
        elif self.current_token.type == TokenType.FUNC:
            return self.func_definition()
        else:
            return self.expr()

    def func_definition(self):
        self.eat(TokenType.FUNC)
        self.eat(TokenType.LPAREN)
        params = []
        # 解析形参
        if self.current_token.type != TokenType.ARROW:
            while True:
                param = self.current_token.value
                self.eat(TokenType.ID)
                params.append(param)
                if self.current_token.type != TokenType.AND:
                    break
                self.eat(TokenType.AND)
        self.eat(TokenType.ARROW)
        func_name = self.current_token.value
        self.eat(TokenType.ID)
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.COLON)

        # 允许换行符或直接进入缩进（兼容单行定义）
        if self.current_token.type == TokenType.NEWLINE:
            self.eat(TokenType.NEWLINE)
            self.eat(TokenType.INDENT)  # 必须缩进

        # 解析函数体
        body = []
        while self.current_token.type != TokenType.DEDENT:
            if self.current_token.type == TokenType.OUT:
                self.eat(TokenType.OUT)
                return_expr = self.expr()
                body.append({'type': 'RETURN', 'value': return_expr})
                break
            else:
                body.append(self.statement())
        self.eat(TokenType.DEDENT)
        return {
            'type': 'FUNC_DEF',
            'name': func_name,
            'params': params,
            'body': body
        }

    def func_call(self):
        args = []
        while self.current_token.type != TokenType.ARROW:
            args.append(self.expr())
            if self.current_token.type == TokenType.AND:
                self.eat(TokenType.AND)
        self.eat(TokenType.ARROW)
        func_name = self.current_token.value
        self.eat(TokenType.ID)
        return {
            'type': 'FUNC_CALL',
            'name': func_name,
            'args': args
        }

    def let_statement(self):
        self.eat(TokenType.LET)
        variables = []
        while True:
            var_name = self.current_token.value
            self.eat(TokenType.ID)
            self.eat(TokenType.COLON)
            value = self.expr()
            variables.append((var_name, value))
            if self.current_token.type != TokenType.AND:
                break
            self.eat(TokenType.AND)
        return {'type': 'LET', 'vars': variables}

    def loop_statement(self):
        self.eat(TokenType.LPAREN)
        # 解析变量部分（单变量或多变量）
        variables = []
        if self.current_token.type == TokenType.LPAREN:  # 多变量，如 (x,y)
            self.eat(TokenType.LPAREN)
            while self.current_token.type == TokenType.ID:
                variables.append(self.current_token.value)
                self.eat(TokenType.ID)
                if self.current_token.type == TokenType.COMMA:
                    self.eat(TokenType.COMMA)
            self.eat(TokenType.RPAREN)
        else:  # 单变量，如 x
            variables.append(self.current_token.value)
            self.eat(TokenType.ID)

        self.eat(TokenType.ARROW)  # 消费 ->
        start = self.expr()  # 起始值
        self.eat(TokenType.AND)  # 消费 &&
        end = self.expr()  # 终止值
        self.eat(TokenType.RPAREN)  # 消费 )
        self.eat(TokenType.DOT)  # 消费 .
        self.eat(TokenType.FOR)  # 消费 for
        self.eat(TokenType.LPAREN)  # 消费 (

        # 直接解析语句，而不是表达式
        body = self.statement()  # 解析循环体（如 say(i)）

        self.eat(TokenType.RPAREN)  # 消费 )
        return {'type': 'FOR_LOOP', 'vars': variables, 'start': start, 'end': end, 'body': body}

    def print_statement(self):
        self.eat(TokenType.PRINT)
        self.eat(TokenType.LPAREN)
        expr_node = self.expr()
        self.eat(TokenType.RPAREN)
        return {'type': 'PRINT', 'expr': expr_node}

    def expr(self):
        if self.current_token.type == TokenType.TABLE:
            return self.table_expr()
        node = self.term()
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            op = self.current_token.type
            self.eat(op)
            node = {
                'type': 'BIN_OP',
                'op': op,
                'left': node,
                'right': self.term()
            }
        return node

    def table_expr(self):
        self.eat(TokenType.TABLE)
        self.eat(TokenType.LPAREN)

        elements = []  # 一维列表元素
        sublists = []  # 多维子列表
        has_semicolon = False  # 标记是否遇到分号

        # 解析第一个元素或子列表
        while self.current_token.type != TokenType.RPAREN:
            # 解析一个元素
            elements.append(self.expr())

            # 处理分隔符：逗号或分号
            if self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
            elif self.current_token.type == TokenType.SEMI:
                has_semicolon = True
                break  # 进入多维列表解析逻辑
            else:
                break  # 无分隔符，结束解析

        if has_semicolon:
            # 存在分号：生成多维列表
            sublists.append(elements)
            while self.current_token.type == TokenType.SEMI:
                self.eat(TokenType.SEMI)
                current_sublist = []
                while True:
                    current_sublist.append(self.expr())
                    if self.current_token.type == TokenType.COMMA:
                        self.eat(TokenType.COMMA)
                    else:
                        break
                sublists.append(current_sublist)
            self.eat(TokenType.RPAREN)
            return {'type': 'TABLE', 'value': sublists}
        else:
            # 无分号：生成一维列表
            self.eat(TokenType.RPAREN)
            return {'type': 'LIST', 'value': elements}  # 新增 LIST 节点类型

    # 解析列表字面量
    def list_expr(self):
        self.eat(TokenType.LBRACKET)
        elements = []
        while self.current_token.type != TokenType.RBRACKET:
            elements.append(self.expr())
            if self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
        self.eat(TokenType.RBRACKET)
        return {'type': 'LIST', 'elements': elements}

    def simple_expr(self):
        token = self.current_token
        if token.type == TokenType.INT:
            self.eat(TokenType.INT)
            return {'type': 'INT', 'value': token.value}
        elif token.type == TokenType.FLOAT:
            self.eat(TokenType.FLOAT)
            return {'type': 'FLOAT', 'value': token.value}
        elif token.type == TokenType.STRING:
            self.eat(TokenType.STRING)
            return {'type': 'STRING', 'value': token.value}
        elif token.type in (TokenType.TRUE, TokenType.FALSE):
            value = token.value
            self.eat(token.type)
            return {'type': 'BOOL', 'value': value}
        elif token.type == TokenType.ID:
            value = token.value
            self.eat(TokenType.ID)
            return {'type': 'VAR', 'value': value}
        else:
            raise Exception("Unexpected token")

    # 解析 enter()
    def enter_expression(self):
        self.eat(TokenType.ENTER)
        self.eat(TokenType.LPAREN)
        self.eat(TokenType.RPAREN)
        return {'type': 'ENTER'}

    # 解析 say(expr)
    def say_statement(self):
        self.eat(TokenType.SAY)
        self.eat(TokenType.LPAREN)
        expr_node = self.expr()
        self.eat(TokenType.RPAREN)
        return {'type': 'SAY', 'expr': expr_node}

    # 解析 endend()
    def endend_statement(self):
        self.eat(TokenType.ENDEND)
        self.eat(TokenType.LPAREN)
        arg = None
        if self.current_token.type == TokenType.INT:
            arg = self.current_token.value
            self.eat(TokenType.INT)
        self.eat(TokenType.RPAREN)
        return {'type': 'ENDEND', 'arg': arg}