<div id="top"></div>

[![OS-Windows]][OS-Windows]
[![OS-Linux]][OS-Linux]
[![OS-MacOS]][OS-MacOS]

<br/>
<div align="center">
<h2 align="center">Nand2Tetris Project 7 - VM Translator</h2>
   <p align="center">
      An .vm to .asm translator written in Python as defined in the Nand2Tetris Project 7.
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
Python 3.13.3 (tags/v3.13.3:6280bb5, Apr  8 2025, 14:47:33) [MSC v.1943 64 bit (AMD64)]

(Tested with Versions 3.12, 3.11, 3.10, 3.9, 3.8, 3.7 and 3.6)
```

### Prerequisites

- Download & Install Python (>= v.3.6):
    - [Python](https://www.python.org/downloads/)

## Usage

```console
trans.py [-h | --help] [<file.vm> | <directory> ...]
```

### Arguments

- -h | --help
    - display help message.
- [\<file.vm\> | \<directory\> ...]
    - provide as many files or directories as you like.
    - files do not need to have the .vm extension (anything else will display a warning).
    - directories will be searched for .vm files.

<p align="right">(<a href="#top">back to top</a>)</p>

## Examples

- e.g.:
    - ```python ./trans.py ./```
    - ```python3 ./trans.py ./```

```bash
   INFO: Searching directory './' for .vm files.
   INFO: File './MemoryAccess\BasicTest\BasicTest.vm' collected.
   INFO: File './MemoryAccess\PointerTest\PointerTest.vm' collected.
   INFO: File './MemoryAccess\StaticTest\StaticTest.vm' collected.
   INFO: File './StackArithmetic\SimpleAdd\SimpleAdd.vm' collected.
   INFO: File './StackArithmetic\StackTest\StackTest.vm' collected.

   INFO: Translating './StackArithmetic\StackTest\StackTest.vm' to './StackArithmetic\StackTest\StackTest.asm'
   INFO: Successfully translated './StackArithmetic\StackTest\StackTest.vm' to './StackArithmetic\StackTest\StackTest.asm'

   INFO: Translating './StackArithmetic\SimpleAdd\SimpleAdd.vm' to './StackArithmetic\SimpleAdd\SimpleAdd.asm'
   INFO: Successfully translated './StackArithmetic\SimpleAdd\SimpleAdd.vm' to './StackArithmetic\SimpleAdd\SimpleAdd.asm'

   INFO: Translating './MemoryAccess\PointerTest\PointerTest.vm' to './MemoryAccess\PointerTest\PointerTest.asm'
   INFO: Successfully translated './MemoryAccess\PointerTest\PointerTest.vm' to './MemoryAccess\PointerTest\PointerTest.asm'

   INFO: Translating './MemoryAccess\StaticTest\StaticTest.vm' to './MemoryAccess\StaticTest\StaticTest.asm'
   INFO: Successfully translated './MemoryAccess\StaticTest\StaticTest.vm' to './MemoryAccess\StaticTest\StaticTest.asm'

   INFO: Translating './MemoryAccess\BasicTest\BasicTest.vm' to './MemoryAccess\BasicTest\BasicTest.asm'
   INFO: Successfully translated './MemoryAccess\BasicTest\BasicTest.vm' to './MemoryAccess\BasicTest\BasicTest.asm'
```

semantic errors are being checked and reported by providing their line number and line content.


```
   INFO: Translating './StackArithmetic\StackTest\StackTest.vm' to './StackArithmetic\StackTest\StackTest.asm'
  ERROR: Unknown command type: 'fizz constant 17' at line 8

   INFO: Translating './StackArithmetic\SimpleAdd\SimpleAdd.vm' to './StackArithmetic\SimpleAdd\SimpleAdd.asm'
  ERROR: Unknown segment for push: 'buzz' at line 9

   INFO: Translating './MemoryAccess\BasicTest\BasicTest.vm' to './MemoryAccess\BasicTest\BasicTest.asm'
  ERROR: Unknown segment for push: 'constant' at line 19

   INFO: Translating './MemoryAccess\StaticTest\StaticTest.vm' to './MemoryAccess\StaticTest\StaticTest.asm'
  ERROR: Invalid index for arg2: '333a' at line 9
```

<p align="right">(<a href="#top">back to top</a>)</p>

## Contact

> **SilenZcience** <br/>
[![GitHub-SilenZcience][GitHub-SilenZcience]](https://github.com/SilenZcience)

[GitHub-SilenZcience]: https://img.shields.io/badge/GitHub-SilenZcience-orange

[OS-Windows]: https://img.shields.io/badge/os-windows-green
[OS-Linux]: https://img.shields.io/badge/os-linux-green
[OS-MacOS]: https://img.shields.io/badge/os-macOS-green
