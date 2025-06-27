<div id="top"></div>

[![OS-Windows]][OS-Windows]
[![OS-Linux]][OS-Linux]
[![OS-MacOS]][OS-MacOS]

<br/>
<div align="center">
<h2 align="center">Nand2Tetris Project 11 - Jack Compiler (Full)</h2>
   <p align="center">
      A .jack to .vm compiler written in Python as defined in the Nand2Tetris Project 11.
   </p>
</div>

<details>
   <summary>Table of Contents</summary>
   <ol>
      <li>
         <a href="#getting-started">Getting Started</a>
         <ul>
            <li><a href="#prerequisites">Prerequisites</a></li>
         </ul>
      </li>
      <li><a href="#usage">Usage</a></li>
         <ul>
            <li><a href="#arguments">Arguments</a></li>
         </ul>
      <li><a href="#examples">Examples</a></li>
      <li><a href="#contact">Contact</a></li>
   </ol>
</details>

## Getting Started

```console
Developed with the following Version Specifications:

Python:
Python 3.13.5 (tags/v3.13.5:6cb20a2, Jun 11 2025, 16:15:46) [MSC v.1943 64 bit (AMD64)]

(Tested with Versions 3.12, 3.11, 3.10, 3.9, 3.8, 3.7 and 3.6)
```

### Prerequisites

- Download & Install Python (>= v.3.6):
    - [Python](https://www.python.org/downloads/)

## Usage

```console
python -m jackCompiler [-h | --help] [<file.jack> | <directory>]
```

### Arguments

- -h | --help
    - display help message.
- [\<file.jack\> | \<directory\>]
    - provide a single .jack file or a single directory.
    - standalone files do not need to have the .jack extension (anything else will display a warning).
    - directories will be searched for .jack files and result in every .jack file being compiled to an .vm file.

<p align="right">(<a href="#top">back to top</a>)</p>

## Examples

- e.g.:
    - ```python -m jackCompiler ./```
    - ```python3 -m jackCompiler ./```

```bash
   INFO: Searching directory '.' for .jack files.
   INFO: File '.\Average\Main.jack' collected.
   INFO: File '.\ComplexArrays\Main.jack' collected.
   INFO: File '.\ConvertToBin\Main.jack' collected.
   INFO: File '.\Pong\Ball.jack' collected.
   INFO: File '.\Pong\Bat.jack' collected.
   INFO: File '.\Pong\Main.jack' collected.
   INFO: File '.\Pong\PongGame.jack' collected.
   INFO: File '.\Seven\Main.jack' collected.
   INFO: File '.\Square\Main.jack' collected.
   INFO: File '.\Square\Square.jack' collected.
   INFO: File '.\Square\SquareGame.jack' collected.

   INFO: Compiling '.\Average\Main.jack'
   INFO: Successfully compiled '.\Average\Main.jack' to '.\Average\Main.vm'

   INFO: Compiling '.\ConvertToBin\Main.jack'
   INFO: Successfully compiled '.\ConvertToBin\Main.jack' to '.\ConvertToBin\Main.vm'

   INFO: Compiling '.\Pong\Ball.jack'
   INFO: Successfully compiled '.\Pong\Ball.jack' to '.\Pong\Ball.vm'

   INFO: Compiling '.\Pong\PongGame.jack'
   INFO: Successfully compiled '.\Pong\PongGame.jack' to '.\Pong\PongGame.vm'

   INFO: Compiling '.\Pong\Main.jack'
   INFO: Successfully compiled '.\Pong\Main.jack' to '.\Pong\Main.vm'

   INFO: Compiling '.\Square\Square.jack'
   INFO: Successfully compiled '.\Square\Square.jack' to '.\Square\Square.vm'

   INFO: Compiling '.\Square\SquareGame.jack'
   INFO: Successfully compiled '.\Square\SquareGame.jack' to '.\Square\SquareGame.vm'

   INFO: Compiling '.\ComplexArrays\Main.jack'
   INFO: Successfully compiled '.\ComplexArrays\Main.jack' to '.\ComplexArrays\Main.vm'

   INFO: Compiling '.\Square\Main.jack'
   INFO: Successfully compiled '.\Square\Main.jack' to '.\Square\Main.vm'

   INFO: Compiling '.\Seven\Main.jack'
   INFO: Successfully compiled '.\Seven\Main.jack' to '.\Seven\Main.vm'

   INFO: Compiling '.\Pong\Bat.jack'
   INFO: Successfully compiled '.\Pong\Bat.jack' to '.\Pong\Bat.vm'
```

errors are being checked and reported by providing their line number.


```
   INFO: Compiling '.\ArrayTest\Main.jack'
  ERROR: Current token is not a keyword!: 'fizz' at line 9

   INFO: Compiling '.\ArrayTest\Main.jack'
  ERROR: Expected 'class', found 'void' at line 9.

   INFO: Compiling '.\ArrayTest\Main.jack'
  ERROR: Expected '(', found '[' at line 10.

   INFO: Compiling '.\ArrayTest\Main.jack'
  ERROR: Expected type (int, char, boolean, or identifier), found '123' at line 11.

  ...

  ERROR: Path '.\ArrayTestFizzBuzz\' is neither a file nor a directory.
```

<p align="right">(<a href="#top">back to top</a>)</p>

## Contact

> **SilenZcience** <br/>
[![GitHub-SilenZcience][GitHub-SilenZcience]](https://github.com/SilenZcience)

[GitHub-SilenZcience]: https://img.shields.io/badge/GitHub-SilenZcience-orange

[OS-Windows]: https://img.shields.io/badge/os-windows-green
[OS-Linux]: https://img.shields.io/badge/os-linux-green
[OS-MacOS]: https://img.shields.io/badge/os-macOS-green
