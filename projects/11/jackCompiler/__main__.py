import os
import sys

from jackCompiler.compilationEngine import CompilationEngine


MSG_ERROR   = '  \x1b[31mERROR\x1b[0m:'
MSG_WARNING = '\x1b[33mWARNING\x1b[0m:'
MSG_INFO    = '   \x1b[32mINFO\x1b[0m:'

NEW_FILE_EXTENSION   = '.vm'


def acc_jack_files(arg_path: str) -> set:
    """
    Collects .jack files from a given path, which can be a file or a directory.
    Returns a set of .jack file paths and their output .vm file path.
    """
    jack_files = set()

    if os.path.isfile(arg_path):
        if os.path.splitext(arg_path)[1] != '.jack':
            print(f"{MSG_WARNING} File '{arg_path}' is not a .jack file.")
        jack_files.add(
            (
                arg_path,
                os.path.splitext(arg_path)[0] + NEW_FILE_EXTENSION,
            )
        )
        print(f"{MSG_INFO} File '{arg_path}' collected.")
        return jack_files

    if os.path.isdir(arg_path):
        print(f"{MSG_INFO} Searching directory '{arg_path}' for .jack files.")
        for root, _, files in os.walk(arg_path):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.splitext(file_path)[1] == '.jack':
                    jack_files.add(
                        (
                            file_path,
                            os.path.splitext(file_path)[0] + NEW_FILE_EXTENSION,
                        )
                    )
                    print(f"{MSG_INFO} File '{file_path}' collected.")
        return jack_files

    raise FileNotFoundError(f"Path '{arg_path}' is neither a file nor a directory.")


def main(args: list) -> int:
    """
    Main function to handle command line arguments and initiate the translation process.
    Expects a single argument which can be a .jack file or a directory containing .jack files.
    """
    if '-h' in args or '--help' in args or len(args) != 1:
        print(f"{MSG_INFO} Usage: python -m jackCompiler [<file.jack> | <directory>]")
        print(f"{MSG_INFO} Translates .jack files to {NEW_FILE_EXTENSION} files.")
        return not len(args) == 1

    try:
        jack_files = acc_jack_files(args[0])
    except FileNotFoundError as e:
        print(f"{MSG_ERROR} {e}")
        return 2
    if not jack_files:
        print(f"{MSG_ERROR} No .jack files found/provided.")
        return 3

    for jack_file, out_file in jack_files:
        print(f"\n{MSG_INFO} Compiling '{jack_file}'")
        try:
            compilation_engine = CompilationEngine(jack_file, out_file)
            compilation_engine.compileClass()
            print(f"{MSG_INFO} Successfully compiled '{jack_file}' to '{out_file}'")
        except (FileNotFoundError, SyntaxError, EOFError) as e:
            print(f"{MSG_ERROR} {e}")
            return 4

    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
