import os
import sys

MSG_ERROR   = '  \x1b[31mERROR\x1b[0m:'
MSG_WARNING = '\x1b[33mWARNING\x1b[0m:'
MSG_INFO    = '   \x1b[32mINFO\x1b[0m:'

COMPS = {
    ''   : '0000000',

    '0'  : '0101010',
    '1'  : '0111111',
    '-1' : '0111010',
    'D'  : '0001100',
    'A'  : '0110000',
    '!D' : '0001101',
    '!A' : '0110001',
    '-D' : '0001111',
    '-A' : '0110011',
    'D+1': '0011111',
    'A+1': '0110111',
    'D-1': '0001110',
    'A-1': '0110010',
    'D+A': '0000010',
    'D-A': '0010011',
    'A-D': '0000111',
    'D&A': '0000000',
    'D|A': '0010101',

    'M'  : '1110000',
    '!M' : '1110001',
    '-M' : '1110011',
    'M+1': '1110111',
    'M-1': '1110010',
    'D+M': '1000010',
    'D-M': '1010011',
    'M-D': '1000111',
    'D&M': '1000000',
    'D|M': '1010101',
}

JUMPS = {
    ''   : '000',
    'JGT': '001',
    'JEQ': '010',
    'JGE': '011',
    'JLT': '100',
    'JNE': '101',
    'JLE': '110',
    'JMP': '111',
}

SYMBOLS = {
    'R0'    :     0,
    'R1'    :     1,
    'R2'    :     2,
    'R3'    :     3,
    'R4'    :     4,
    'R5'    :     5,
    'R6'    :     6,
    'R7'    :     7,
    'R8'    :     8,
    'R9'    :     9,
    'R10'   :    10,
    'R11'   :    11,
    'R12'   :    12,
    'R13'   :    13,
    'R14'   :    14,
    'R15'   :    15,

    'SCREEN': 16384,
    'KDB'   : 24576,

    'SP'    :     0,
    'LCL'   :     1,
    'ARG'   :     2,
    'THIS'  :     3,
    'THAT'  :     4,
}


class Assembler:
    """
    Assembler class to translate .asm files to .hack files.
    """

    def __init__(self, in_file: str) -> None:
        self.in_file = in_file
        self.vars, self.labels = {}, {}
        self.current_var_id = 16

    def _clean_file(self) -> list:
        """
        Clean the file from comments, whitespaces and empty lines and
        collect labels.
        """
        asm_instructs = []
        with open(self.in_file, 'r', encoding='utf-8') as f_open:
            for lineno, line in enumerate(f_open, start=1):
                c_line = line.split('//')[0].strip()
                if c_line.startswith('('):
                    if not c_line.endswith(')'):
                        raise SyntaxError(f"Invalid label format in line {lineno}: {c_line}")
                    label_name = c_line[1:-1]
                    self.labels[label_name] = len(asm_instructs)
                elif c_line:
                    asm_instructs.append((c_line, lineno))
        return asm_instructs

    def _translate_instructions(self, asm_instructs: list) -> list:
        """
        Translate the instructions to binary format.
        """
        bin_instructs = []
        for line, lineno in asm_instructs:
            if line.startswith('@'):
                target = line[1:]
                if target.isdigit():
                    address = int(target)
                    if address > (1 << 15):
                        print(f"{MSG_WARNING} Address '{address}' exceeds 15 bits in line {lineno}: {line}")
                        address = 16 # no idea why, but this is the behaviour of the original assembler
                else:
                    if target in self.labels:
                        address = self.labels[target]
                    elif target in SYMBOLS:
                        address = SYMBOLS[target]
                    else:
                        if target not in self.vars:
                            self.vars[target] = self.current_var_id
                            self.current_var_id += 1
                        address = self.vars[target]
                bin_instructs.append(f"0{address:015b}")
                continue

            dst, rst = line.split('=') if '=' in line else ('', line)
            cmp, jmp = rst.split(";") if ';' in rst else (rst, '')
            dst_bits = ('1' if 'A' in dst else '0') + ('1' if 'D' in dst else '0') + ('1' if 'M' in dst else '0')
            comp = COMPS.get(cmp, None)
            if comp is None:
                raise SyntaxError(f"Invalid comp '{cmp}' in line {lineno}: {line}")
            jump = JUMPS.get(jmp, None)
            if jump is None:
                raise SyntaxError(f"Invalid jump '{jmp}' in line {lineno}: {line}")
            bin_instructs.append('111' + comp + dst_bits + jump)
        return bin_instructs

    def assemble(self, out_file: str) -> None:
        asm_instructs = self._clean_file()
        bin_instructs = self._translate_instructions(asm_instructs)
        with open(out_file, 'w', encoding='utf-8') as f_open:
            f_open.writelines([f"{instruct}\n" for instruct in bin_instructs])


def acc_asm_files(arg_paths: list) -> set:
    asm_files = set()
    for path in arg_paths:
        if os.path.isfile(path):
            filename, file_extension = os.path.splitext(path)
            if file_extension != '.asm':
                print(f"{MSG_WARNING} File '{path}' is not a .asm file.")
            asm_files.add((path, filename + '.hack'))
            print(f"{MSG_INFO} File '{path}' collected.")
            continue
        if os.path.isdir(path):
            print(f"{MSG_INFO} Searching directory '{path}' for .asm files.")
            for root, _, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    filename, file_extension = os.path.splitext(file_path)
                    if file_extension == '.asm':
                        asm_files.add((file_path, filename + '.hack'))
                        print(f"{MSG_INFO} File '{file_path}' collected.")
    return asm_files


def main(args: list) -> int:
    if '-h' in args or '--help' in args:
        print(f"{MSG_INFO} Usage: python {sys.argv[0]} [<file.asm> | <directory> ...]")
        print(f"{MSG_INFO} Assembles .asm files to .hack files.")
        return 0
    asm_files: set = acc_asm_files(args)
    if not asm_files:
        print(f"{MSG_ERROR} No .asm files found/provided.")
        return 1
    for in_file, out_file in asm_files:
        print(f"\n{MSG_INFO} Assembling '{in_file}' to '{out_file}'")
        try:
            Assembler(in_file).assemble(out_file)
            print(f"{MSG_INFO} Successfully assembled '{in_file}' to '{out_file}'")
        except SyntaxError as e:
            print(f"{MSG_ERROR} {e}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
