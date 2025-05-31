import os
import sys

from vmtranslator.vm_parser import VMParser, CTypes
from vmtranslator.vm_codewriter import VMCodeWriter


MSG_ERROR   = '  \x1b[31mERROR\x1b[0m:'
MSG_WARNING = '\x1b[33mWARNING\x1b[0m:'
MSG_INFO    = '   \x1b[32mINFO\x1b[0m:'


CODEWRITER_CALLS = {
    CTypes.C_ARITHMETIC: 'writeArithmetic',
    CTypes.C_PUSH:       'writePush',
    CTypes.C_POP:        'writePop',
    CTypes.C_LABEL:      'writeLabel',
    CTypes.C_GOTO:       'writeGoto',
    CTypes.C_IF:         'writeIf',
    CTypes.C_FUNCTION:   'writeFunction',
    CTypes.C_CALL:       'writeCall',
    CTypes.C_RETURN:     'writeReturn'
}


class VMTranslator:
    def __init__(self, out_file: str, include_init: bool) -> None:
        self.out_file = out_file
        self.codewriter: VMCodeWriter = VMCodeWriter(out_file)
        if include_init:
            self.codewriter.writeInit()

    def translate(self, in_file: str):
        parser: VMParser = VMParser(in_file)
        self.codewriter.setCurrentFileName(in_file)

        while parser.hasMoreLines():
            parser.advance()
            command_type = parser.commandType()
            self.codewriter.setCurrentLine(parser.commandLine())

            getattr(
                self.codewriter,
                CODEWRITER_CALLS[command_type],
                lambda *_: None
            )(
                parser.arg1(),
                parser.arg2()
            )


def acc_vm_files(arg_path: str) -> tuple:
    """
    Collects .vm files from a given path, which can be a file or a directory.
    Returns a set of .vm file paths and the output assembly file path.
    """
    vm_files = set()

    if os.path.isfile(arg_path):
        if os.path.splitext(arg_path)[1] != '.vm':
            print(f"{MSG_WARNING} File '{arg_path}' is not a .vm file.")
        vm_files.add(arg_path)
        print(f"{MSG_INFO} File '{arg_path}' collected.")
        return vm_files, os.path.splitext(arg_path)[0] + '.asm'

    if os.path.isdir(arg_path):
        print(f"{MSG_INFO} Searching directory '{arg_path}' for .vm files.")
        for root, _, files in os.walk(arg_path):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.splitext(file_path)[1] == '.vm':
                    vm_files.add(file_path)
                    print(f"{MSG_INFO} File '{file_path}' collected.")
        return vm_files, os.path.join(arg_path, os.path.basename(os.path.normpath(arg_path)) + '.asm')

    raise FileNotFoundError(f"Path '{arg_path}' is neither a file nor a directory.")


def contains_sys_init(vm_files):
    """
    Check if any of the provided .vm files contains a 'Sys.init' call.
    If true we need to generate the bootstrap code in the output assembly file.
    """
    for vm_file in vm_files:
        with open(vm_file, encoding="utf-8") as f:
            if "Sys.init" in f.read():
                return True
    return False


def main(args: list) -> int:
    if '-h' in args or '--help' in args or len(args) != 1:
        print(f"{MSG_INFO} Usage: python -m vmtranslator [<file.vm> | <directory>]")
        print(f"{MSG_INFO} Translates .vm files to a single .asm file.")
        return not len(args) == 1

    try:
        vm_files, out_file = acc_vm_files(args[0])
    except FileNotFoundError as e:
        print(f"{MSG_ERROR} {e}")
        return 2
    if not vm_files:
        print(f"{MSG_ERROR} No .vm files found/provided.")
        return 3

    vm_translator = VMTranslator(out_file, include_init=contains_sys_init(vm_files))
    for vm_file in vm_files:
        print(f"\n{MSG_INFO} Translating '{vm_file}'")
        try:
            vm_translator.translate(vm_file)
            print(f"{MSG_INFO} Successfully translated '{vm_file}'")
        except (FileNotFoundError, SyntaxError, EOFError) as e:
            print(f"{MSG_ERROR} {e}")
            del vm_translator
            return 4
    print(f"\n{MSG_INFO} Translation complete. Output written to '{out_file}'")

    del vm_translator
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
