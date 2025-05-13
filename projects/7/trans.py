import os
import sys

from vm_parser import VMParser
from vm_codewriter import VMCodeWriter


MSG_ERROR   = '  \x1b[31mERROR\x1b[0m:'
MSG_WARNING = '\x1b[33mWARNING\x1b[0m:'
MSG_INFO    = '   \x1b[32mINFO\x1b[0m:'


class VMTranslator:
    def __init__(self, in_file: str) -> None:
        self.in_file = in_file

    def translate(self, out_file: str):
        parser: VMParser = VMParser(self.in_file)
        codewriter: VMCodeWriter = VMCodeWriter(out_file)
        while parser.hasMoreLines():
            parser.advance()
            command_type = parser.commandType()
            c_line = parser.commandLine()
            if command_type == 'C_ARITHMETIC':
                codewriter.writeArithmetic(c_line, parser.arg1())
            elif command_type in ['C_PUSH', 'C_POP']:
                codewriter.writePushPop(c_line, command_type, parser.arg1(), parser.arg2())
            else:
                raise SyntaxError(f"Unknown command type: '{parser.instruction}' at line {c_line}")


def acc_vm_files(arg_paths: list) -> set:
    asm_files = set()
    for path in arg_paths:
        if os.path.isfile(path):
            filename, file_extension = os.path.splitext(path)
            if file_extension != '.vm':
                print(f"{MSG_WARNING} File '{path}' is not a .vm file.")
            asm_files.add((path, filename + '.asm'))
            print(f"{MSG_INFO} File '{path}' collected.")
            continue
        if os.path.isdir(path):
            print(f"{MSG_INFO} Searching directory '{path}' for .vm files.")
            for root, _, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    filename, file_extension = os.path.splitext(file_path)
                    if file_extension == '.vm':
                        asm_files.add((file_path, filename + '.asm'))
                        print(f"{MSG_INFO} File '{file_path}' collected.")
    return asm_files


def main(args: list) -> int:
    if '-h' in args or '--help' in args:
        print(f"{MSG_INFO} Usage: python {sys.argv[0]} [<file.vm> | <directory> ...]")
        print(f"{MSG_INFO} Translates .vm files to .asm files.")
        return 0
    vm_files: set = acc_vm_files(args)
    if not vm_files:
        print(f"{MSG_ERROR} No .vm files found/provided.")
        return 1
    for in_file, out_file in vm_files:
        print(f"\n{MSG_INFO} Translating '{in_file}' to '{out_file}'")
        try:
            VMTranslator(in_file).translate(out_file)
            print(f"{MSG_INFO} Successfully translated '{in_file}' to '{out_file}'")
        except (SyntaxError, EOFError) as e:
            print(f"{MSG_ERROR} {e}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
