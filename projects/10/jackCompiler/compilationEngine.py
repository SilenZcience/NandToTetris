
from jackCompiler.jackTokenizer import JackTokenizer, TTypes, KTypes


COMPILE_OP_MAP = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
}


class CompilationEngine:
    def __init__(self, jack_file: str, out_file: str, token_file: str):
        self.jack_file = jack_file
        self.out_file = out_file
        self.f_out_file = open(out_file, 'w', encoding='utf-8')
        self.token_file = token_file
        self.f_token_file = open(token_file, 'w', encoding='utf-8')

        self.tokenizer = JackTokenizer(jack_file)
        self.indent = 0

    def raiseException(self, message: str) -> None:
        """
        Raises a SyntaxError with the given message.
        """
        self.f_out_file.close()
        self.f_token_file.close()
        raise SyntaxError(message)

    def writeFile(self, content: str) -> None:
        """
        Writes content to the specified stream with indentation.
        """
        self.f_out_file.write(' ' * self.indent + content + '\n')

    def writeKeyword(self, keyword: KTypes) -> None:
        """
        Writes a keyword to the output file with proper indentation.
        """
        self.writeFile(f'<keyword> {keyword.value} </keyword>')
        self.f_token_file.write(f'<keyword> {keyword.value} </keyword>\n')
        self.tokenizer.advance()

    def writeSymbol(self, symbol: str) -> None:
        """
        Writes a symbol to the output file with proper indentation.
        """
        self.writeFile(f'<symbol> {symbol} </symbol>')
        self.f_token_file.write(f'<symbol> {symbol} </symbol>\n')
        self.tokenizer.advance()

    def writeInteger(self, integer: int) -> None:
        """
        Writes an integer to the output file with proper indentation.
        """
        self.writeFile(f'<integerConstant> {integer} </integerConstant>')
        self.f_token_file.write(f'<integerConstant> {integer} </integerConstant>\n')
        self.tokenizer.advance()

    def writeString(self, string: str) -> None:
        """
        Writes a string to the output file with proper indentation.
        """
        self.writeFile(f'<stringConstant> {string} </stringConstant>')
        self.f_token_file.write(f'<stringConstant> {string} </stringConstant>\n')
        self.tokenizer.advance()

    def writeIdentifier(self, identifier: str) -> None:
        """
        Writes an identifier to the output file with proper indentation.
        """
        self.writeFile(f'<identifier> {identifier} </identifier>')
        self.f_token_file.write(f'<identifier> {identifier} </identifier>\n')
        self.tokenizer.advance()

    def compileClass(self) -> None:
        self.writeFile('<class>')
        self.indent += 2
        self.f_token_file.write('<tokens>\n')

        if self.tokenizer.keyWord() != KTypes.K_CLASS:
            self.raiseException(f"Expected 'class', found '{self.tokenizer.token[0]}' at line {self.tokenizer.token[1]}.")
        self.writeKeyword(self.tokenizer.keyWord())

        self.compileClassName()

        if self.tokenizer.symbol() != '{':
            self.raiseException("Expected '{', found " + f"'{self.tokenizer.token[0]}' at line {self.tokenizer.token[1]}.")
        self.writeSymbol(self.tokenizer.symbol())

        while self.tokenizer.tokenType() == TTypes.T_KEYWORD and self.tokenizer.keyWord() in (KTypes.K_STATIC, KTypes.K_FIELD):
            self.compileClassVarDec()

        while self.tokenizer.tokenType() == TTypes.T_KEYWORD and self.tokenizer.keyWord() in (KTypes.K_CONSTRUCTOR, KTypes.K_FUNCTION, KTypes.K_METHOD):
            self.compileSubroutineDec()

        if self.tokenizer.symbol() != '}':
            self.raiseException("Expected '}', found " + f"'{self.tokenizer.token[0]}' at line {self.tokenizer.token[1]}.")
        self.writeSymbol(self.tokenizer.symbol())

        self.indent -= 2
        self.writeFile('</class>')
        self.f_token_file.write('</tokens>\n')

        if self.tokenizer.hasMoreTokens():
            self.raiseException(f"Unexpected tokens after class definition in '{self.jack_file}' at line {self.tokenizer.token[1]}.")

        self.f_out_file.close()
        self.f_token_file.close()

    def compileClassVarDec(self) -> None:
        self.writeFile('<classVarDec>')
        self.indent += 2
        self.writeKeyword(self.tokenizer.keyWord())

        self.compileType()

        self.compileVarName()

        while self.tokenizer.tokenType() == TTypes.T_SYMBOL and self.tokenizer.symbol() == ',':
            self.writeSymbol(self.tokenizer.symbol())
            self.compileVarName()

        if self.tokenizer.symbol() != ';':
            self.raiseException(f"Expected ';', found '{self.tokenizer.token[0]}' at line {self.tokenizer.token[1]}.")
        self.writeSymbol(self.tokenizer.symbol())

        self.indent -= 2
        self.writeFile('</classVarDec>')

    def compileType(self) -> None:
        if self.tokenizer.tokenType() == TTypes.T_KEYWORD and self.tokenizer.keyWord() in (KTypes.K_INT, KTypes.K_CHAR, KTypes.K_BOOLEAN):
            self.writeKeyword(self.tokenizer.keyWord())
        elif self.tokenizer.tokenType() == TTypes.T_IDENTIFIER:
            self.compileClassName()
        else:
            self.raiseException(f"Expected type (int, char, boolean, or identifier), found '{self.tokenizer.token[0]}' at line {self.tokenizer.token[1]}.")

    def compileSubroutineDec(self) -> None:
        self.writeFile('<subroutineDec>')
        self.indent += 2
        self.writeKeyword(self.tokenizer.keyWord())

        if self.tokenizer.tokenType() == TTypes.T_KEYWORD and self.tokenizer.keyWord() == KTypes.K_VOID:
            self.writeKeyword(self.tokenizer.keyWord())
        else:
            self.compileType()

        self.compileSubroutineName()

        if self.tokenizer.symbol() != '(':
            self.raiseException(f"Expected '(', found '{self.tokenizer.token[0]}' at line {self.tokenizer.token[1]}.")
        self.writeSymbol(self.tokenizer.symbol())

        self.compileParameterList()

        if self.tokenizer.symbol() != ')':
            self.raiseException(f"Expected ')', found '{self.tokenizer.token[0]}' at line {self.tokenizer.token[1]}.")
        self.writeSymbol(self.tokenizer.symbol())

        self.compileSubroutineBody()

        self.indent -= 2
        self.writeFile('</subroutineDec>')

    def compileParameterList(self) -> None:
        self.writeFile('<parameterList>')
        self.indent += 2

        if self.tokenizer.tokenType() != TTypes.T_SYMBOL or self.tokenizer.symbol() != ')':
            self.compileType()
            self.compileVarName()

            while self.tokenizer.tokenType() == TTypes.T_SYMBOL and self.tokenizer.symbol() == ',':
                self.writeSymbol(self.tokenizer.symbol())
                self.compileType()
                self.compileVarName()

        self.indent -= 2
        self.writeFile('</parameterList>')

    def compileSubroutineBody(self) -> None:
        self.writeFile('<subroutineBody>')
        self.indent += 2

        if self.tokenizer.symbol() != '{':
            self.raiseException("Expected '{', found " + f"'{self.tokenizer.token[0]}' at line {self.tokenizer.token[1]}.")
        self.writeSymbol(self.tokenizer.symbol())

        while self.tokenizer.tokenType() == TTypes.T_KEYWORD and self.tokenizer.keyWord() == KTypes.K_VAR:
            self.compileVarDec()

        self.compileStatements()

        if self.tokenizer.symbol() != '}':
            self.raiseException("Expected '}', found " + f"'{self.tokenizer.token[0]}' at line {self.tokenizer.token[1]}.")
        self.writeSymbol(self.tokenizer.symbol())

        self.indent -= 2
        self.writeFile('</subroutineBody>')

    def compileVarDec(self) -> None:
        self.writeFile('<varDec>')
        self.indent += 2
        self.writeKeyword(self.tokenizer.keyWord())

        self.compileType()

        self.compileVarName()

        while self.tokenizer.tokenType() == TTypes.T_SYMBOL and self.tokenizer.symbol() == ',':
            self.writeSymbol(self.tokenizer.symbol())
            self.compileVarName()

        if self.tokenizer.symbol() != ';':
            self.raiseException(f"Expected ';', found '{self.tokenizer.token[0]}' at line {self.tokenizer.token[1]}.")
        self.writeSymbol(self.tokenizer.symbol())

        self.indent -= 2
        self.writeFile('</varDec>')

    def compileClassName(self) -> None:
        self.writeIdentifier(self.tokenizer.identifier())

    def compileSubroutineName(self) -> None:
        self.writeIdentifier(self.tokenizer.identifier())

    def compileVarName(self) -> None:
        self.writeIdentifier(self.tokenizer.identifier())

    def compileStatements(self) -> None:
        self.writeFile('<statements>')
        self.indent += 2

        while self.tokenizer.tokenType() == TTypes.T_KEYWORD and self.tokenizer.keyWord() in (KTypes.K_LET, KTypes.K_IF, KTypes.K_WHILE, KTypes.K_DO, KTypes.K_RETURN):
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

        self.indent -= 2
        self.writeFile('</statements>')

    def compileLetStatement(self) -> None:
        self.writeFile('<letStatement>')
        self.indent += 2
        self.writeKeyword(self.tokenizer.keyWord())

        self.compileVarName()

        if self.tokenizer.tokenType() == TTypes.T_SYMBOL and self.tokenizer.symbol() == '[':
            self.writeSymbol(self.tokenizer.symbol())
            self.compileExpression()
            if self.tokenizer.symbol() != ']':
                self.raiseException(f"Expected ']', found '{self.tokenizer.token[0]}' at line {self.tokenizer.token[1]}.")
            self.writeSymbol(self.tokenizer.symbol())

        if self.tokenizer.symbol() != '=':
            self.raiseException(f"Expected '=', found '{self.tokenizer.token[0]}' at line {self.tokenizer.token[1]}.")
        self.writeSymbol(self.tokenizer.symbol())

        self.compileExpression()

        if self.tokenizer.symbol() != ';':
            self.raiseException(f"Expected ';', found '{self.tokenizer.token[0]}' at line {self.tokenizer.token[1]}.")
        self.writeSymbol(self.tokenizer.symbol())

        self.indent -= 2
        self.writeFile('</letStatement>')

    def compileIfStatement(self) -> None:
        self.writeFile('<ifStatement>')
        self.indent += 2
        self.writeKeyword(self.tokenizer.keyWord())

        if self.tokenizer.symbol() != '(':
            self.raiseException(f"Expected '(', found '{self.tokenizer.token[0]}' at line {self.tokenizer.token[1]}.")
        self.writeSymbol(self.tokenizer.symbol())

        self.compileExpression()

        if self.tokenizer.symbol() != ')':
            self.raiseException(f"Expected ')', found '{self.tokenizer.token[0]}' at line {self.tokenizer.token[1]}.")
        self.writeSymbol(self.tokenizer.symbol())

        if self.tokenizer.symbol() != '{':
            self.raiseException("Expected '{', found " + f"'{self.tokenizer.token[0]}' at line {self.tokenizer.token[1]}.")
        self.writeSymbol(self.tokenizer.symbol())

        self.compileStatements()

        if self.tokenizer.symbol() != '}':
            self.raiseException("Expected '}', found " + f"'{self.tokenizer.token[0]}' at line {self.tokenizer.token[1]}.")
        self.writeSymbol(self.tokenizer.symbol())

        if self.tokenizer.tokenType() == TTypes.T_KEYWORD and self.tokenizer.keyWord() == KTypes.K_ELSE:
            self.writeKeyword(self.tokenizer.keyWord())
            if self.tokenizer.symbol() != '{':
                self.raiseException("Expected '{', found " + f"'{self.tokenizer.token[0]}' at line {self.tokenizer.token[1]}.")
            self.writeSymbol(self.tokenizer.symbol())
            self.compileStatements()
            if self.tokenizer.symbol() != '}':
                self.raiseException("Expected '}', found " + f"'{self.tokenizer.token[0]}' at line {self.tokenizer.token[1]}.")
            self.writeSymbol(self.tokenizer.symbol())

        self.indent -= 2
        self.writeFile('</ifStatement>')

    def compileWhileStatement(self) -> None:
        self.writeFile('<whileStatement>')
        self.indent += 2
        self.writeKeyword(self.tokenizer.keyWord())

        if self.tokenizer.symbol() != '(':
            self.raiseException(f"Expected '(', found '{self.tokenizer.token[0]}' at line {self.tokenizer.token[1]}.")
        self.writeSymbol(self.tokenizer.symbol())

        self.compileExpression()

        if self.tokenizer.symbol() != ')':
            self.raiseException(f"Expected ')', found '{self.tokenizer.token[0]}' at line {self.tokenizer.token[1]}.")
        self.writeSymbol(self.tokenizer.symbol())

        if self.tokenizer.symbol() != '{':
            self.raiseException("Expected '{', found " + f"'{self.tokenizer.token[0]}' at line {self.tokenizer.token[1]}.")
        self.writeSymbol(self.tokenizer.symbol())

        self.compileStatements()

        if self.tokenizer.symbol() != '}':
            self.raiseException("Expected '}', found " + f"'{self.tokenizer.token[0]}' at line {self.tokenizer.token[1]}.")
        self.writeSymbol(self.tokenizer.symbol())

        self.indent -= 2
        self.writeFile('</whileStatement>')

    def compileDoStatement(self) -> None:
        self.writeFile('<doStatement>')
        self.indent += 2
        self.writeKeyword(self.tokenizer.keyWord())

        self.compileVarName()
        self.compileSubroutineCall()

        if self.tokenizer.symbol() != ';':
            self.raiseException(f"Expected ';', found '{self.tokenizer.token[0]}' at line {self.tokenizer.token[1]}.")
        self.writeSymbol(self.tokenizer.symbol())

        self.indent -= 2
        self.writeFile('</doStatement>')

    def compileReturnStatement(self) -> None:
        self.writeFile('<returnStatement>')
        self.indent += 2
        self.writeKeyword(self.tokenizer.keyWord())

        if self.tokenizer.tokenType() != TTypes.T_SYMBOL:
            self.compileExpression()

        if self.tokenizer.symbol() != ';':
            self.raiseException(f"Expected ';', found '{self.tokenizer.token[0]}' at line {self.tokenizer.token[1]}.")
        self.writeSymbol(self.tokenizer.symbol())

        self.indent -= 2
        self.writeFile('</returnStatement>')

    def compileExpression(self) -> None:
        self.writeFile('<expression>')
        self.indent += 2

        self.compileTerm()

        while self.tokenizer.tokenType() == TTypes.T_SYMBOL and self.tokenizer.symbol() in ('+', '-', '*', '/', '&', '|', '<', '>', '='):
            self.compileOp()
            self.compileTerm()

        self.indent -= 2
        self.writeFile('</expression>')

    def compileTerm(self) -> None:
        self.writeFile('<term>')
        self.indent += 2

        if self.tokenizer.tokenType() == TTypes.T_INTEGER:
            self.writeInteger(self.tokenizer.intVal())
        elif self.tokenizer.tokenType() == TTypes.T_STRING:
            self.writeString(self.tokenizer.stringVal())
        elif self.tokenizer.tokenType() == TTypes.T_KEYWORD and self.tokenizer.keyWord() in (KTypes.K_TRUE, KTypes.K_FALSE, KTypes.K_NULL, KTypes.K_THIS):
            self.compileKeywordConstant()
        elif self.tokenizer.tokenType() == TTypes.T_IDENTIFIER:
            self.compileVarName()
            if self.tokenizer.tokenType() == TTypes.T_SYMBOL and self.tokenizer.symbol() == '[':
                self.writeSymbol(self.tokenizer.symbol())
                self.compileExpression()
                if self.tokenizer.symbol() != ']':
                    self.raiseException(f"Expected ']', found '{self.tokenizer.token[0]}' at line {self.tokenizer.token[1]}.")
                self.writeSymbol(self.tokenizer.symbol())
            elif self.tokenizer.tokenType() == TTypes.T_SYMBOL and self.tokenizer.symbol() in ('.', '('):
                self.compileSubroutineCall()
        elif self.tokenizer.tokenType() == TTypes.T_SYMBOL and self.tokenizer.symbol() == '(':
            self.writeSymbol(self.tokenizer.symbol())
            self.compileExpression()
            if self.tokenizer.symbol() != ')':
                self.raiseException(f"Expected ')', found '{self.tokenizer.token[0]}' at line {self.tokenizer.token[1]}.")
            self.writeSymbol(self.tokenizer.symbol())
        elif self.tokenizer.tokenType() == TTypes.T_SYMBOL and self.tokenizer.symbol() in ('-', '~'):
            self.compileUnaryOp()
            self.compileTerm()
        else:
            raise SyntaxError(f"Unexpected token: '{self.tokenizer.token[0]}' at line {self.tokenizer.token[1]}.")

        self.indent -= 2
        self.writeFile('</term>')

    def compileSubroutineCall(self) -> None:
        if self.tokenizer.symbol() == '.':
            self.writeSymbol(self.tokenizer.symbol())
            self.compileSubroutineName()
        if self.tokenizer.symbol() != '(':
            self.raiseException(f"Expected '(', found '{self.tokenizer.token[0]}' at line {self.tokenizer.token[1]}.")
        self.writeSymbol(self.tokenizer.symbol())
        self.compileExpressionList()
        if self.tokenizer.symbol() != ')':
            self.raiseException(f"Expected ')', found '{self.tokenizer.token[0]}' at line {self.tokenizer.token[1]}.")
        self.writeSymbol(self.tokenizer.symbol())

    def compileExpressionList(self) -> None:
        self.writeFile('<expressionList>')
        self.indent += 2

        if self.tokenizer.tokenType() != TTypes.T_SYMBOL or self.tokenizer.symbol() == '(':
            self.compileExpression()

            while self.tokenizer.tokenType() == TTypes.T_SYMBOL and self.tokenizer.symbol() == ',':
                self.writeSymbol(self.tokenizer.symbol())
                self.compileExpression()

        self.indent -= 2
        self.writeFile('</expressionList>')

    def compileOp(self) -> None:
        self.writeSymbol(COMPILE_OP_MAP.get(self.tokenizer.symbol(), self.tokenizer.symbol()))

    def compileUnaryOp(self) -> None:
        self.writeSymbol(self.tokenizer.symbol())

    def compileKeywordConstant(self) -> None:
        self.writeKeyword(self.tokenizer.keyWord())
