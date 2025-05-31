<div id="top"></div>

[![OS-Windows]][OS-Windows]
[![OS-Linux]][OS-Linux]
[![OS-MacOS]][OS-MacOS]

<br/>
<div align="center">
<h2 align="center">Nand2Tetris Project 8 - VM Translator</h2>
   <p align="center">
      A .vm to .asm translator written in Python as defined in the Nand2Tetris Project 8.
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
python -m vmtranslator [-h | --help] [<file.vm> | <directory>]
```

### Arguments

- -h | --help
    - display help message.
- [\<file.vm\> | \<directory\>]
    - provide a single .vm file or a single directory.
    - standalone files do not need to have the .vm extension (anything else will display a warning).
    - directories will be searched for .vm files and result in one single merged .asm file.

<p align="right">(<a href="#top">back to top</a>)</p>

## Examples

- e.g.:
    - ```python -m vmtranslator ./FunctionCalls/StaticsTest/```
    - ```python3 -m vmtranslator ./FunctionCalls/StaticsTest/```

```bash
   INFO: Searching directory './FunctionCalls/StaticsTest/' for .vm files.
   INFO: File './FunctionCalls/StaticsTest/Class1.vm' collected.
   INFO: File './FunctionCalls/StaticsTest/Class2.vm' collected.
   INFO: File './FunctionCalls/StaticsTest/Sys.vm' collected.

   INFO: Translating './FunctionCalls/StaticsTest/Class1.vm'
   INFO: Successfully translated './FunctionCalls/StaticsTest/Class1.vm'

   INFO: Translating './FunctionCalls/StaticsTest/Class2.vm'
   INFO: Successfully translated './FunctionCalls/StaticsTest/Class2.vm'

   INFO: Translating './FunctionCalls/StaticsTest/Sys.vm'
   INFO: Successfully translated './FunctionCalls/StaticsTest/Sys.vm'

   INFO: Translation complete. Output written to './FunctionCalls/StaticsTest/StaticsTest.asm'
```

semantic errors are being checked and reported by providing their line number and line content.


```
   INFO: Translating './FunctionCalls/StaticsTest/Class1.vm'
  ERROR: Wrong number of arguments for command 'push argument 0 fizz' at line 8

   INFO: Translating './FunctionCalls/StaticsTest/Class1.vm'
  ERROR: Unknown command type: 'buzz' at line 9

   INFO: Translating './FunctionCalls/StaticsTest/Class1.vm'
  ERROR: Unknown segment for push: 'fizzbuzz' at line 8

   INFO: Translating './FunctionCalls/StaticsTest/Class1.vm'
  ERROR: Unknown segment for pop: 'constant' at line 8

   INFO: Translating './FunctionCalls/StaticsTest/Class1.vm'
  ERROR: Invalid index for second argument: '0x00' at line 8

  ERROR: Path './FunctionCalls/StaticsTests/' is neither a file nor a directory.
```

<p align="right">(<a href="#top">back to top</a>)</p>

## Contact

> **SilenZcience** <br/>
[![GitHub-SilenZcience][GitHub-SilenZcience]](https://github.com/SilenZcience)

[GitHub-SilenZcience]: https://img.shields.io/badge/GitHub-SilenZcience-orange

[OS-Windows]: https://img.shields.io/badge/os-windows-green
[OS-Linux]: https://img.shields.io/badge/os-linux-green
[OS-MacOS]: https://img.shields.io/badge/os-macOS-green
