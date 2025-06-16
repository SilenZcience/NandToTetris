
from jackCompiler.jackTokenizer import JackTokenizer


class CompilationEngine:
    def __init__(self, jack_file: str, out_file: str, token_file: str):
        self.jack_file = jack_file
        self.out_file = out_file
        self.token_file = token_file

        self.tokenizer = JackTokenizer(jack_file)

    def compileClass(self) -> None:
        pass

    def compileClassVarDec(self) -> None:
        pass

    def compileSubroutine(self) -> None:
        pass

    def compileParameterList(self) -> None:
        pass

    def compileVarDec(self) -> None:
        pass

    def compileStatements(self) -> None:
        pass

    def compileDo(self) -> None:
        pass

    def compileLet(self) -> None:
        pass

    def compileWhile(self) -> None:
        pass

    def compileReturn(self) -> None:
        pass

    def compileIf(self) -> None:
        pass

    def compileExpression(self) -> None:
        pass

    def compileTerm(self) -> None:
        pass

    def compileExpressionList(self) -> None:
        pass
