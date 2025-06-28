from jackCompiler.jackTokenizer import JackTokenizer, TTypes, KTypes
from jackCompiler.symbolTable import SymbolTable, VarKind


class CompilationEngine:
    def __init__(self, jack_file: str, out_file: str):
        self.jack_file = jack_file
        self.f_out_file = open(out_file, 'w', encoding='utf-8')

        self.tokenizer = JackTokenizer(jack_file)
        self.s_table = SymbolTable()

        self.c_class_name = ''
        self.c_subroutine_name = ''
        self.label_id = 0

    def raise_expection(self, message: str) -> None:
        """
        Raises a SyntaxError with the given message.
        Closes file handles before raising the exception.
        """
        self.f_out_file.close()
        raise SyntaxError(message)

    @property
    def label_name(self) -> str:
        """
        Generates a unique label name (for if and while statements).
        """
        label = f"{self.c_class_name}.{self.c_subroutine_name}.LABEL_{self.label_id}"
        self.label_id += 1
        return label

    def write(self, content: str) -> None:
        """
        Writes content to the specified stream with indentation.
        """
        if not (content.startswith('label') or content.startswith('function')):
            self.f_out_file.write('    ')
        self.f_out_file.write(content + '\n')

    def check_keyword(self, keyword: KTypes) -> None:
        """
        Checks if the current token is the expected keyword.
        """
        if self.tokenizer.keyWord() != keyword:
            self.raise_expection(f"Expected keyword '{keyword.value}', found '{self.tokenizer.token[0]}' at line {self.tokenizer.token[1]}.")
        self.tokenizer.advance()

    def check_symbol(self, symbol: str) -> None:
        """
        Checks if the current token is the expected symbol.
        """
        if self.tokenizer.symbol() != symbol:
            self.raise_expection(f"Expected symbol '{symbol}', found '{self.tokenizer.token[0]}' at line {self.tokenizer.token[1]}.")
        self.tokenizer.advance()

    def compileClass(self) -> None:
        """
        class: 'class' className '{' classVarDec* subroutineDec* '}'
        """
        self.check_keyword(KTypes.K_CLASS)

        self.c_class_name = self.tokenizer.identifier()
        self.tokenizer.advance()

        self.check_symbol('{')

        while self.tokenizer.tokenType() == TTypes.T_KEYWORD and self.tokenizer.keyWord() in (KTypes.K_STATIC, KTypes.K_FIELD):
            self.compileClassVarDec()

        while self.tokenizer.tokenType() == TTypes.T_KEYWORD and self.tokenizer.keyWord() in (KTypes.K_CONSTRUCTOR, KTypes.K_FUNCTION, KTypes.K_METHOD):
            self.compileSubroutineDec()

        self.check_symbol('}')

        if self.tokenizer.hasMoreTokens():
            self.raise_expection(f"Unexpected tokens after class definition in '{self.jack_file}' at line {self.tokenizer.token[1]}.")
        self.f_out_file.close()

    def compileClassVarDec(self) -> None:
        """
        classVarDec: ('static' | 'field') type varName (',' varName)* ';'
        """
        c_kind = VarKind.STATIC if (self.tokenizer.keyWord() == KTypes.K_STATIC) else VarKind.FIELD
        self.tokenizer.advance()

        c_type = self.compileType()

        self.s_table.add(self.tokenizer.identifier(), c_type, c_kind)
        self.tokenizer.advance()

        while self.tokenizer.tokenType() == TTypes.T_SYMBOL and self.tokenizer.symbol() == ',':
            self.tokenizer.advance()
            self.s_table.add(self.tokenizer.identifier(), c_type, c_kind)
            self.tokenizer.advance()

        self.check_symbol(';')

    def compileType(self) -> str:
        """
        type: 'int' | 'char' | 'boolean' | className
        """
        c_type: str = ''
        if self.tokenizer.tokenType() == TTypes.T_KEYWORD and self.tokenizer.keyWord() in (KTypes.K_INT, KTypes.K_CHAR, KTypes.K_BOOLEAN):
            c_type = self.tokenizer.keyWord().value
        elif self.tokenizer.tokenType() == TTypes.T_IDENTIFIER:
            c_type = self.tokenizer.identifier()
        else:
            self.raise_expection(f"Expected type (int, char, boolean, or identifier), found '{self.tokenizer.token[0]}' at line {self.tokenizer.token[1]}.")
        self.tokenizer.advance()
        return c_type

    def compileSubroutineDec(self) -> None:
        """
        subroutineDec: ('constructor' | 'function' | 'method') (type | 'void') subroutineName '(' parameterList ')' subroutineBody
        """
        self.s_table.start_subroutine()

        c_keyword = self.tokenizer.keyWord()
        if c_keyword == KTypes.K_METHOD:
            self.s_table.add('this', self.c_class_name, VarKind.ARG)
        self.tokenizer.advance()

        if self.tokenizer.tokenType() == TTypes.T_KEYWORD and self.tokenizer.keyWord() == KTypes.K_VOID:
            self.tokenizer.advance()
        else:
            self.compileType()

        self.c_subroutine_name = self.tokenizer.identifier()
        self.tokenizer.advance()

        self.check_symbol('(')

        self.compileParameterList()

        self.check_symbol(')')

        self.compileSubroutineBody(c_keyword)

    def compileParameterList(self) -> None:
        """
        parameterList: (type varName (',' type varName)*)?
        """
        if self.tokenizer.tokenType() != TTypes.T_SYMBOL or self.tokenizer.symbol() != ')':
            c_type = self.compileType()
            self.s_table.add(self.tokenizer.identifier(), c_type, VarKind.ARG)
            self.tokenizer.advance()

            while self.tokenizer.tokenType() == TTypes.T_SYMBOL and self.tokenizer.symbol() == ',':
                self.tokenizer.advance()
                c_type = self.compileType()
                self.s_table.add(self.tokenizer.identifier(), c_type, VarKind.ARG)
                self.tokenizer.advance()

    def compileSubroutineBody(self, c_keyword: KTypes) -> None:
        """
        subroutineBody: '{' varDec* statements '}'
        """
        self.check_symbol('{')

        while self.tokenizer.tokenType() == TTypes.T_KEYWORD and self.tokenizer.keyWord() == KTypes.K_VAR:
            self.compileVarDec()

        self.write(f"function {self.c_class_name}.{self.c_subroutine_name} {self.s_table.get_max_index(VarKind.LOCAL)}")
        if c_keyword == KTypes.K_CONSTRUCTOR:
            self.write(f"push constant {self.s_table.get_max_index(VarKind.FIELD)}")
            self.write('call Memory.alloc 1')
            self.write('pop pointer 0')
        elif c_keyword == KTypes.K_METHOD:
            self.write('push argument 0')
            self.write('pop pointer 0')

        self.compileStatements()

        self.check_symbol('}')

    def compileVarDec(self) -> None:
        """
        varDec: 'var' type varName (',' varName)* ';'s
        """
        self.tokenizer.advance()

        c_type = self.compileType()

        self.s_table.add(self.tokenizer.identifier(), c_type, VarKind.LOCAL)
        self.tokenizer.advance()

        while self.tokenizer.tokenType() == TTypes.T_SYMBOL and self.tokenizer.symbol() == ',':
            self.tokenizer.advance()
            self.s_table.add(self.tokenizer.identifier(), c_type, VarKind.LOCAL)
            self.tokenizer.advance()

        self.check_symbol(';')

    def compileStatements(self) -> None:
        """
        statements: statement*
        """
        while self.tokenizer.tokenType() == TTypes.T_KEYWORD and \
            self.tokenizer.keyWord() in (KTypes.K_LET, KTypes.K_IF, KTypes.K_WHILE, KTypes.K_DO, KTypes.K_RETURN):
            keyword = self.tokenizer.keyWord()
            if keyword == KTypes.K_LET:
                self.compileLetStatement()
            elif keyword == KTypes.K_IF:
                self.compileIfStatement()
            elif keyword == KTypes.K_WHILE:
                self.compileWhileStatement()
            elif keyword == KTypes.K_DO:
                self.compileDoStatement()
            elif keyword == KTypes.K_RETURN:
                self.compileReturnStatement()

    def compileLetStatement(self) -> None:
        """
        letStatement: 'let' varName ('[' expression ']')? '=' expression ';'
        """
        self.tokenizer.advance()

        c_varName = self.tokenizer.identifier()
        self.tokenizer.advance()
        isArray = False

        if self.tokenizer.tokenType() == TTypes.T_SYMBOL and self.tokenizer.symbol() == '[':
            isArray = True
            self.tokenizer.advance()
            self.write(f"push {SymbolTable.get_segment(self.s_table.get_info(c_varName, SymbolTable.VAR_KIND))} {self.s_table.get_info(c_varName, SymbolTable.VAR_INDEX)}")
            self.compileExpression()
            self.check_symbol(']')
            self.write('add')

        self.check_symbol('=')

        self.compileExpression()

        if isArray:
            self.write('pop temp 0')
            self.write('pop pointer 1')
            self.write('push temp 0')
            self.write('pop that 0')
        else:
            self.write(f"pop {SymbolTable.get_segment(self.s_table.get_info(c_varName, SymbolTable.VAR_KIND))} {self.s_table.get_info(c_varName, SymbolTable.VAR_INDEX)}")

        self.check_symbol(';')

    def compileIfStatement(self) -> None:
        """
        ifStatement: 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
        """
        label_a, label_b = self.label_name, self.label_name
        self.tokenizer.advance()

        self.check_symbol('(')

        self.compileExpression()

        self.check_symbol(')')

        self.write('not')
        self.write(f'if-goto {label_a}')

        self.check_symbol('{')

        self.compileStatements()

        self.check_symbol('}')

        self.write(f'goto {label_b}')
        self.write(f'label {label_a}')

        if self.tokenizer.tokenType() == TTypes.T_KEYWORD and self.tokenizer.keyWord() == KTypes.K_ELSE:
            self.tokenizer.advance()
            self.check_symbol('{')
            self.compileStatements()
            self.check_symbol('}')

        self.write(f"label {label_b}")

    def compileWhileStatement(self) -> None:
        """
        whileStatement: 'while' '(' expression ')' '{' statements '}'
        """
        label_a, label_b = self.label_name, self.label_name
        self.tokenizer.advance()

        self.write(f'label {label_a}')

        self.check_symbol('(')

        self.compileExpression()

        self.check_symbol(')')

        self.write('not')
        self.write(f'if-goto {label_b}')

        self.check_symbol('{')

        self.compileStatements()

        self.check_symbol('}')

        self.write(f'goto {label_a}')
        self.write(f'label {label_b}')

    def compileDoStatement(self) -> None:
        """
        doStatement: 'do' subroutineCall ';'
        """
        self.tokenizer.advance()

        c_varName = self.tokenizer.identifier()
        self.tokenizer.advance()

        self.compileSubroutineCall(c_varName)

        self.check_symbol(';')

        self.write('pop temp 0')

    def compileReturnStatement(self) -> None:
        """
        returnStatement: 'return' expression? ';'
        """
        self.tokenizer.advance()

        if self.tokenizer.tokenType() != TTypes.T_SYMBOL:
            self.compileExpression()
        else:
            self.write('push constant 0')

        self.check_symbol(';')

        self.write('return')

    def compileExpression(self) -> None:
        """
        expression: term (op term)*
        """
        self.compileTerm()

        while self.tokenizer.tokenType() == TTypes.T_SYMBOL and \
            self.tokenizer.symbol() in ('+', '-', '*', '/', '&', '|', '<', '>', '='):
            c_op = self.compileOp()

            self.compileTerm()
            self.write(f"{c_op}")

    def compileTerm(self) -> None:
        """
        term: integerConstant | stringConstant | keywordConstant | varName | varName '[' expression ']' | subroutineCall | '(' expression ')' | unaryOp term
        """
        if self.tokenizer.tokenType() == TTypes.T_INTEGER:

            self.write(f"push constant {self.tokenizer.intVal()}")
            self.tokenizer.advance()

        elif self.tokenizer.tokenType() == TTypes.T_STRING:

            c_string = self.tokenizer.stringVal()
            self.write(f"push constant {len(c_string)}")
            self.write('call String.new 1')
            for char in c_string:
                self.write(f"push constant {ord(char)}")
                self.write('call String.appendChar 2')
            self.tokenizer.advance()

        elif self.tokenizer.tokenType() == TTypes.T_KEYWORD and \
            self.tokenizer.keyWord() in (KTypes.K_TRUE, KTypes.K_FALSE, KTypes.K_NULL, KTypes.K_THIS):

            self.write(f"push {'pointer' if (self.tokenizer.keyWord() == KTypes.K_THIS) else 'constant'} 0")
            if self.tokenizer.keyWord() == KTypes.K_TRUE:
                self.write('not')
            self.tokenizer.advance()

        elif self.tokenizer.tokenType() == TTypes.T_IDENTIFIER:

            c_varName = self.tokenizer.identifier()
            self.tokenizer.advance()

            if self.tokenizer.tokenType() == TTypes.T_SYMBOL and self.tokenizer.symbol() == '[':
                self.tokenizer.advance()

                self.write(f"push {SymbolTable.get_segment(self.s_table.get_info(c_varName, SymbolTable.VAR_KIND))} {self.s_table.get_info(c_varName, SymbolTable.VAR_INDEX)}")
                self.compileExpression()

                self.check_symbol(']')

                self.write('add')
                self.write('pop pointer 1')
                self.write('push that 0')
            elif self.tokenizer.tokenType() == TTypes.T_SYMBOL and self.tokenizer.symbol() in ('.', '('):
                self.compileSubroutineCall(c_varName)
            else:
                self.write(f"push {SymbolTable.get_segment(self.s_table.get_info(c_varName, SymbolTable.VAR_KIND))} {self.s_table.get_info(c_varName, SymbolTable.VAR_INDEX)}")

        elif self.tokenizer.tokenType() == TTypes.T_SYMBOL and self.tokenizer.symbol() == '(':
            self.tokenizer.advance()

            self.compileExpression()

            self.check_symbol(')')

        elif self.tokenizer.tokenType() == TTypes.T_SYMBOL and self.tokenizer.symbol() in ('-', '~'):

            c_op = self.compileUnaryOp()

            self.compileTerm()
            self.write(f"{c_op}")
        else:
            raise SyntaxError(f"Unexpected token: '{self.tokenizer.token[0]}' at line {self.tokenizer.token[1]}.")


    def compileSubroutineCall(self, c_identifier: str) -> None:
        """
        subroutineCall: subroutineName '(' expressionList ')' | (className | varName) '.' subroutineName '(' expressionList ')'
        """
        if self.tokenizer.symbol() == '(':
            self.tokenizer.advance()
            self.write('push pointer 0')

            arg_count = self.compileExpressionList()

            self.check_symbol(')')

            self.write(f"call {self.c_class_name}.{c_identifier} {arg_count + 1}")
        elif self.tokenizer.symbol() == '.':
            self.tokenizer.advance()

            c_subroutine_name = self.tokenizer.identifier()
            self.tokenizer.advance()

            arg_count = 0
            c_type = self.s_table.get_info(c_identifier, SymbolTable.VAR_TYPE)
            if c_type:
                if c_type in ('int', 'char', 'boolean'):
                    self.raise_expection(f"Cannot call method on primitive type '{c_type}' at line {self.tokenizer.token[1]}.")
                else:
                    self.write(f"push {SymbolTable.get_segment(self.s_table.get_info(c_identifier, SymbolTable.VAR_KIND))} {self.s_table.get_info(c_identifier, SymbolTable.VAR_INDEX)}")
                    arg_count += 1
                    c_identifier = c_type

            self.check_symbol('(')

            arg_count += self.compileExpressionList()

            self.check_symbol(')')

            self.write(f"call {c_identifier}.{c_subroutine_name} {arg_count}")
        else:
            self.raise_expection(f"Expected '(' or '.', found '{self.tokenizer.token[0]}' at line {self.tokenizer.token[1]}.")

    def compileExpressionList(self) -> int:
        """
        expressionList: (expression (',' expression)*)?
        """
        arg_count = 0

        if self.tokenizer.tokenType() != TTypes.T_SYMBOL or self.tokenizer.symbol() == '(':
            self.compileExpression()
            arg_count += 1

            while self.tokenizer.tokenType() == TTypes.T_SYMBOL and self.tokenizer.symbol() == ',':
                self.tokenizer.advance()

                self.compileExpression()
                arg_count += 1

        return arg_count

    def compileOp(self) -> str:
        """
        op: '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
        """
        c_op = self.tokenizer.symbol()
        self.tokenizer.advance()
        if c_op == '+':
            return 'add'
        if c_op == '-':
            return 'sub'
        if c_op == '*':
            return 'call Math.multiply 2'
        if c_op == '/':
            return 'call Math.divide 2'
        if c_op == '&':
            return 'and'
        if c_op == '|':
            return 'or'
        if c_op == '<':
            return 'lt'
        if c_op == '>':
            return 'gt'
        if c_op == '=':
            return 'eq'
        self.raise_expection(f"Unknown operator: '{c_op}' at line {self.tokenizer.token[1]}.")

    def compileUnaryOp(self) -> str:
        """
        unaryOp: '-' | '~'
        """
        c_op = self.tokenizer.symbol()
        self.tokenizer.advance()
        if c_op == '-':
            return 'neg'
        if c_op == '~':
            return 'not'
        self.raise_expection(f"Unknown operator: '{c_op}' at line {self.tokenizer.token[1]}.")
