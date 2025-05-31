from enum import Enum


class CTypes(Enum):
    """
    Enum for command types in VM files.
    """
    C_ARITHMETIC = 'C_ARITHMETIC'
    C_PUSH = 'C_PUSH'
    C_POP = 'C_POP'
    C_LABEL = 'C_LABEL'
    C_GOTO = 'C_GOTO'
    C_IF = 'C_IF'
    C_FUNCTION = 'C_FUNCTION'
    C_CALL = 'C_CALL'
    C_RETURN = 'C_RETURN'


class VMParser:
    """
    A simple parser for .vm files.
    """
    def __init__(self, in_file: str) -> None:
        self.in_file = in_file
        self.position = -1
        self.instructions = []
        self.instruction: tuple = ('', 0) # (instruction, line number)

        self._read_instructions()

    def _read_instructions(self) -> None:
        with open(self.in_file, 'r', encoding='utf-8') as f_in:
            for i, line in enumerate(f_in, start=1):
                line = line.split('//')[0].strip()
                if line:
                    self.instructions.append((line, i))

    def hasMoreLines(self) -> bool:
        """
        check if there are more lines to read.
        """
        return self.position < len(self.instructions)-1

    def advance(self) -> None:
        """
        read the next line and set it as the current instruction.
        """
        if not self.hasMoreLines():
            raise EOFError("No more lines to read.")
        self.position += 1
        self.instruction = self.instructions[self.position]

    def commandType(self) -> str:
        """
        return the type of the current command.
        """
        instruction_parts = self.instruction[0].split(' ')
        instruction = instruction_parts[0]
        if instruction in ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']:
            return CTypes.C_ARITHMETIC
        if instruction == 'push':
            return CTypes.C_PUSH
        if instruction == 'pop':
            return CTypes.C_POP
        if instruction == 'label':
            return CTypes.C_LABEL
        if instruction == 'goto':
            return CTypes.C_GOTO
        if instruction == 'if-goto':
            return CTypes.C_IF
        if instruction == 'function':
            return CTypes.C_FUNCTION
        if instruction == 'call':
            return CTypes.C_CALL
        if instruction == 'return':
            return CTypes.C_RETURN
        raise SyntaxError(f"Unknown command type: '{self.instruction[0]}' at line {self.instruction[1]}")

    def commandLine(self) -> int:
        """
        return the line number of the current command.
        """
        return self.instruction[1]

    def arg1(self) -> str:
        """
        return the first argument of the current command.
        """
        instruction_parts = self.instruction[0].split(' ')
        if self.commandType() == CTypes.C_RETURN:
            return None
        if self.commandType() == CTypes.C_ARITHMETIC:
            return instruction_parts[0]
        return instruction_parts[1]

    def arg2(self) -> int:
        """
        return the second argument of the current command.
        """
        instruction_parts = self.instruction[0].split(' ')
        if self.commandType() in [CTypes.C_PUSH, CTypes.C_POP, CTypes.C_FUNCTION, CTypes.C_CALL]:
            if len(instruction_parts) != 3:
                raise SyntaxError(f"Wrong number of arguments for command '{self.instruction[0]}' at line {self.instruction[1]}")
            if not instruction_parts[2].isdigit():
                raise SyntaxError(f"Invalid index for second argument: '{instruction_parts[2]}' at line {self.instruction[1]}")
            return int(instruction_parts[2])
        return None
