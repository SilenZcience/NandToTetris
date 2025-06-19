import re
from enum import Enum


class TTypes(Enum):
    """
    Enum for token types.
    """
    T_KEYWORD     = 'keyword'
    T_SYMBOL      = 'symbol'
    T_INTEGER     = 'integerConstant'
    T_STRING      = 'stringConstant'
    T_IDENTIFIER  = 'identifier'

class KTypes(Enum):
    """
    Enum for keyword types in jack files.
    """
    K_CLASS       = 'class'
    K_CONSTRUCTOR = 'constructor'
    K_FUNCTION    = 'function'
    K_METHOD      = 'method'
    K_FIELD       = 'field'
    K_STATIC      = 'static'
    K_VAR         = 'var'
    K_INT         = 'int'
    K_CHAR        = 'char'
    K_BOOLEAN     = 'boolean'
    K_VOID        = 'void'
    K_TRUE        = 'true'
    K_FALSE       = 'false'
    K_NULL        = 'null'
    K_THIS        = 'this'
    K_LET         = 'let'
    K_DO          = 'do'
    K_IF          = 'if'
    K_ELSE        = 'else'
    K_WHILE       = 'while'
    K_RETURN      = 'return'

KTYPES_MAP = {k.value: k for k in KTypes}


PATTERN_BLOCK_COMMENT = re.compile(r'/\*.*?\*/', re.DOTALL)
PATTERN_KEYWORD       = re.compile(r'|'.join([t.value for t in KTypes]))
PATTERN_SYMBOL        = re.compile(r'[\{\}\(\)\[\]\.\,\;\+\-\*\/\&\|\<\>\=\~]')
PATTERN_INTEGER       = re.compile(r'\d+')
PATTERN_STRING        = re.compile(r'\"[^\"\r\n]*?\"')
PATTERN_IDENTIFIER    = re.compile(r'[a-zA-Z_]\w*')
PATTERN_TOKEN         = re.compile(
    PATTERN_KEYWORD.pattern + r'|' + \
    PATTERN_SYMBOL.pattern  + r'|' + \
    PATTERN_INTEGER.pattern + r'|' + \
    PATTERN_STRING.pattern  + r'|' + \
    PATTERN_IDENTIFIER.pattern
)


class JackTokenizer:
    """
    A simple tokenizer for .jack files.
    """
    def __init__(self, in_file: str) -> None:
        self.in_file = in_file
        self.position = -1
        self.tokens = []
        self.token: tuple = ('', 0) # (token, line number)

        self._read_tokens()
        self.advance()  # Initialize the first token

    def _read_tokens(self) -> None:
        """
        read tokens from the input file and store them in self.tokens.
        It removes comments and splits the code into tokens.
        It also keeps track of the line numbers for each token by
        replacing multilinecomments with newlines.
        """
        def replacer(match):
            comment = match.group(0)
            return '\n' * comment.count('\n')

        jack_code = ''
        with open(self.in_file, 'r', encoding='utf-8') as f_in:
            for line in f_in:
                line = line.split('//')[0].strip()
                jack_code += line + '\n'
        jack_code = re.sub(PATTERN_BLOCK_COMMENT, replacer, jack_code)

        line_starts = [0]
        for m in re.finditer(r'\n', jack_code):
            line_starts.append(m.end())

        line_num = 1
        for match in re.finditer(PATTERN_TOKEN, jack_code):
            while match.start() >= line_starts[line_num]:
                line_num += 1
            self.tokens.append((match.group(0), line_num))

        self.tokens.append(None) # one last token to indicate EOF and make the compilationEngine easier

    def hasMoreTokens(self) -> bool:
        """
        checks if there are more tokens to process.
        """
        return self.position < len(self.tokens)-1

    def advance(self) -> None:
        """
        advances the current token to the next one.
        """
        if not self.hasMoreTokens():
            raise EOFError("No more tokens to read.")
        self.position += 1
        self.token = self.tokens[self.position]

    def tokenType(self) -> TTypes:
        """
        returns the type of the current token.
        """
        token = self.token[0]
        if PATTERN_KEYWORD.match(token):
            return TTypes.T_KEYWORD
        if PATTERN_SYMBOL.match(token):
            return TTypes.T_SYMBOL
        if PATTERN_INTEGER.match(token):
            return TTypes.T_INTEGER
        if PATTERN_STRING.match(token):
            return TTypes.T_STRING
        if PATTERN_IDENTIFIER.match(token):
            return TTypes.T_IDENTIFIER
        raise SyntaxError(f"Unknown token type: '{token}' at line {self.token[1]}")

    def keyWord(self) -> KTypes:
        """
        returns the keyword which is the current token.
        """
        if self.tokenType() != TTypes.T_KEYWORD:
            raise SyntaxError(f"Current token is not a keyword: '{self.token[0]}' at line {self.token[1]}")
        return KTYPES_MAP.get(self.token[0])

    def symbol(self) -> str:
        """
        returns the character which is the current token.
        """
        if self.tokenType() != TTypes.T_SYMBOL:
            raise SyntaxError(f"Current token is not a symbol: '{self.token[0]}' at line {self.token[1]}")
        return self.token[0]

    def identifier(self) -> str:
        """
        returns the identifier which is the current token.
        """
        if self.tokenType() != TTypes.T_IDENTIFIER:
            raise SyntaxError(f"Current token is not an identifier: '{self.token[0]}' at line {self.token[1]}")
        return self.token[0]

    def intVal(self) -> int:
        """
        returns the integer value which is the current token.
        """
        if self.tokenType() != TTypes.T_INTEGER:
            raise SyntaxError(f"Current token is not an integer: '{self.token[0]}' at line {self.token[1]}")
        return int(self.token[0])

    def stringVal(self) -> str:
        """
        returns the string value which is the current token.
        """
        if self.tokenType() != TTypes.T_STRING:
            raise SyntaxError(f"Current token is not a string: '{self.token[0]}' at line {self.token[1]}")
        return self.token[0][1:-1]
