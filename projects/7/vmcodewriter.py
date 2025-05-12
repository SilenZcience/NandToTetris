


ASM_CODE_ADD = """// add
@SP
AM=M-1
D=M
A=A-1
M=M+D
"""
ASM_CODE_SUB = """// sub
@SP
AM=M-1
D=M
A=A-1
M=M-D
"""
ASM_CODE_NEG = """// neg
@SP
A=M-1
M=-M
"""
ASM_CODE_EQ = """// eq
"""
ASM_CODE_GT = """// gt
"""
ASM_CODE_LT = """// lt
"""
ASM_CODE_AND = """// and
@SP
AM=M-1
D=M
A=A-1
M=M&D
"""
ASM_CODE_OR = """// or
@SP
AM=M-1
D=M
A=A-1
M=M|D
"""
ASM_CODE_NOT = """// not
@SP
A=M-1
M=!M
"""

class VMCodeWriter:
    def __init__(self, out_file: str) -> None:
        self.out_file = out_file
        with open(self.out_file, 'w', encoding='utf-8') as f_out:
            f_out.write('// VM Code Writer written by Silas Kraume\n\n')

    def writeArithmetic(self, command: str) -> None:
        """
        Write the assembly code for the arithmetic command.
        """
        with open(self.out_file, 'a', encoding='utf-8') as f_out:
            if command == 'add':
                f_out.write(ASM_CODE_ADD)
            elif command == 'sub':
                f_out.write(ASM_CODE_SUB)
            elif command == 'neg':
                f_out.write(ASM_CODE_NEG)
            elif command == 'eq':
                f_out.write(ASM_CODE_EQ)
            elif command == 'gt':
                f_out.write(ASM_CODE_GT)
            elif command == 'lt':
                f_out.write(ASM_CODE_LT)
            elif command == 'and':
                f_out.write(ASM_CODE_AND)
            elif command == 'or':
                f_out.write(ASM_CODE_OR)
            elif command == 'not':
                f_out.write(ASM_CODE_NOT)
            else:
                raise SyntaxError(f"Unknown arithmetic command: {command}")


    def writePushPop(self, command: str, segment: str, index: int) -> None:
        """
        Write the assembly code for the push/pop command.
        """
        with open(self.out_file, 'a', encoding='utf-8') as f_out:
            if command not in ['C_PUSH', 'C_POP']:
                raise SyntaxError(f"Unknown command type for push/pop: {command}")
            if command == 'C_PUSH':
                if segment not in ['constant', 'local', 'argument', 'this', 'that', 'static', 'temp', 'pointer']:
                    raise SyntaxError(f"Unknown segment for push: {segment}")
                if segment == 'constant':
                    f_out.write(f"// push {segment} {index}\n")
                    f_out.write(f"@{index}\n")
                    f_out.write("D=A\n")
                    f_out.write("@SP\n")
                    f_out.write("A=M\n")
                    f_out.write("M=D\n")
                    f_out.write("@SP\n")
                    f_out.write("M=M+1\n")
                elif segment == 'local':
                    f_out.write(f"// push {segment} {index}\n")
                    f_out.write(f"@{index}\n")
                    f_out.write("D=A\n")
                    f_out.write("@LCL\n")
                    f_out.write("A=D+M\n")
                    f_out.write("D=M\n")
                    f_out.write("@SP\n")
                    f_out.write("A=M\n")
                    f_out.write("M=D\n")
                    f_out.write("@SP\n")
                    f_out.write("M=M+1\n")
                elif segment == 'argument':
                    f_out.write(f"// push {segment} {index}\n")
                    f_out.write(f"@{index}\n")
                    f_out.write("D=A\n")
                    f_out.write("@ARG\n")
                    f_out.write("A=D+M\n")
                    f_out.write("D=M\n")
                    f_out.write("@SP\n")
                    f_out.write("A=M\n")
                    f_out.write("M=D\n")
                    f_out.write("@SP\n")
                    f_out.write("M=M+1\n")
                elif segment == 'this':
                    f_out.write(f"// push {segment} {index}\n")
                    f_out.write(f"@{index}\n")
                    f_out.write("D=A\n")
                    f_out.write("@THIS\n")
                    f_out.write("A=D+M\n")
                    f_out.write("D=M\n")
                    f_out.write("@SP\n")
                    f_out.write("A=M\n")
                    f_out.write("M=D\n")
                    f_out.write("@SP\n")
                    f_out.write("M=M+1\n")
                elif segment == 'that':
                    f_out.write(f"// push {segment} {index}\n")
                    f_out.write(f"@{index}\n")
                    f_out.write("D=A\n")
                    f_out.write("@THAT\n")
                    f_out.write("A=D+M\n")
                    f_out.write("D=M\n")
                    f_out.write("@SP\n")
                    f_out.write("A=M\n")
                    f_out.write("M=D\n")
                    f_out.write("@SP\n")
                    f_out.write("M=M+1\n")
                elif segment == 'static':
                    f_out.write(f"// push {segment} {index}\n")
                    f_out.write(f"@{index + 16}\n")
                    f_out.write("D=M\n")
                    f_out.write("@SP\n")
                    f_out.write("A=M\n")
                    f_out.write("M=D\n")
                    f_out.write("@SP\n")
                    f_out.write("M=M+1\n")
                elif segment == 'temp':
                    f_out.write(f"// push {segment} {index}\n")
                    f_out.write(f"@{index + 5}\n")
                    f_out.write("D=M\n")
                    f_out.write("@SP\n")
                    f_out.write("A=M\n")
                    f_out.write("M=D\n")
                    f_out.write("@SP\n")
                    f_out.write("M=M+1\n")
                elif segment == 'pointer':
                    f_out.write(f"// push {segment} {index}\n")
                    f_out.write(f"@{index + 3}\n")
                    f_out.write("D=M\n")
                    f_out.write("@SP\n")
                    f_out.write("A=M\n")
                    f_out.write("M=D\n")
                    f_out.write("@SP\n")
                    f_out.write("M=M+1\n")
            elif command == 'C_POP':
                if segment not in ['local', 'argument', 'this', 'that', 'static', 'temp', 'pointer']:
                    raise SyntaxError(f"Unknown segment for push: {segment}")
                if segment == 'local':
                    f_out.write(f"// pop {segment} {index}\n")
                    f_out.write(f"@{index}\n")
                    f_out.write("D=A\n")
                    f_out.write("@LCL\n")
                    f_out.write("D=D+M\n")
                    f_out.write("@R13\n")
                    f_out.write("M=D\n")
                    f_out.write("@SP\n")
                    f_out.write("AM=M-1\n")
                    f_out.write("D=M\n")
                    f_out.write("@R13\n")
                    f_out.write("A=M\n")
                    f_out.write("M=D\n")
                elif segment == 'argument':
                    f_out.write(f"// pop {segment} {index}\n")
                    f_out.write(f"@{index}\n")
                    f_out.write("D=A\n")
                    f_out.write("@ARG\n")
                    f_out.write("D=D+M\n")
                    f_out.write("@R13\n")
                    f_out.write("M=D\n")
                    f_out.write("@SP\n")
                    f_out.write("AM=M-1\n")
                    f_out.write("D=M\n")
                    f_out.write("@R13\n")
                    f_out.write("A=M\n")
                    f_out.write("M=D\n")
                elif segment == 'this':
                    f_out.write(f"// pop {segment} {index}\n")
                    f_out.write(f"@{index}\n")
                    f_out.write("D=A\n")
                    f_out.write("@THIS\n")
                    f_out.write("D=D+M\n")
                    f_out.write("@R13\n")
                    f_out.write("M=D\n")
                    f_out.write("@SP\n")
                    f_out.write("AM=M-1\n")
                    f_out.write("D=M\n")
                    f_out.write("@R13\n")
                    f_out.write("A=M\n")
                    f_out.write("M=D\n")
                elif segment == 'that':
                    f_out.write(f"// pop {segment} {index}\n")
                    f_out.write(f"@{index}\n")
                    f_out.write("D=A\n")
                    f_out.write("@THAT\n")
                    f_out.write("D=D+M\n")
                    f_out.write("@R13\n")
                    f_out.write("M=D\n")
                    f_out.write("@SP\n")
                    f_out.write("AM=M-1\n")
                    f_out.write("D=M\n")
                    f_out.write("@R13\n")
                    f_out.write("A=M\n")
                    f_out.write("M=D\n")
                elif segment == 'static':
                    f_out.write(f"// pop {segment} {index}\n")
                    f_out.write(f"@{index + 16}\n")
                    f_out.write("D=A\n")
                    f_out.write("@R13\n")
                    f_out.write("M=D\n")
                    f_out.write("@SP\n")
                    f_out.write("AM=M-1\n")
                    f_out.write("D=M\n")
                    f_out.write("@R13\n")
                    f_out.write("A=M\n")
                    f_out.write("M=D\n")
                elif segment == 'temp':
                    f_out.write(f"// pop {segment} {index}\n")
                    f_out.write(f"@{index + 5}\n")
                    f_out.write("D=A\n")
                    f_out.write("@R13\n")
                    f_out.write("M=D\n")
                    f_out.write("@SP\n")
                    f_out.write("AM=M-1\n")
                    f_out.write("D=M\n")
                    f_out.write("@R13\n")
                    f_out.write("A=M\n")
                    f_out.write("M=D\n")
                elif segment == 'pointer':
                    f_out.write(f"// pop {segment} {index}\n")
                    f_out.write(f"@{index + 3}\n")
                    f_out.write("D=A\n")
                    f_out.write("@R13\n")
                    f_out.write("M=D\n")
                    f_out.write("@SP\n")
                    f_out.write("AM=M-1\n")
                    f_out.write("D=M\n")
                    f_out.write("@R13\n")
                    f_out.write("A=M\n")
                    f_out.write("M=D\n")
