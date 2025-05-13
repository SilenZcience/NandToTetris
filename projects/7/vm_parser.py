

class VMParser:
    """
    A simple parser for .vm files.
    """
    def __init__(self, in_file: str) -> None:
        self.in_file = in_file
        self.position = -1
        self.instructions = []
        self.instruction: tuple = ('', 0)

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

    def commandType(self) -> str: # the lazy mans enum :)
        """
        return the type of the current command.
        """
        instruction_parts = self.instruction[0].split(' ')
        instruction = instruction_parts[0]
        if instruction in ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']:
            return 'C_ARITHMETIC'
        if instruction == 'push':
            return 'C_PUSH'
        if instruction == 'pop':
            return 'C_POP'
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
        if self.commandType() == 'C_ARITHMETIC':
            return instruction_parts[0]
        if self.commandType() in ['C_PUSH', 'C_POP']:
            return instruction_parts[1]
        raise SyntaxError(f"Invalid command type for arg1: '{self.instruction[0]}' at line {self.instruction[1]}")

    def arg2(self) -> int:
        """
        return the second argument of the current command.
        """
        instruction_parts = self.instruction[0].split(' ')
        if self.commandType() in ['C_PUSH', 'C_POP']:
            if not instruction_parts[2].isdigit():
                raise SyntaxError(f"Invalid index for arg2: '{instruction_parts[2]}' at line {self.instruction[1]}")
            return int(instruction_parts[2])
        raise SyntaxError(f"Invalid command type for arg2: '{self.instruction[0]}' at line {self.instruction[1]}")
