<div id="top"></div>

[![OS-Windows]][OS-Windows]
[![OS-Linux]][OS-Linux]
[![OS-MacOS]][OS-MacOS]

<br/>
<div align="center">
<h2 align="center">Nand2Tetris Project 6 - Assembler</h2>
   <p align="center">
      An .asm to .hack assembler written in Python as defined in the Nand2Tetris Project 6.
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
ass.py [-h | --help] [<file.asm> | <directory> ...]
```

### Arguments

- -h | --help
    - display help message.
- [\<file.asm\> | \<directory\> ...]
    - provide as many files or directories as you like.
    - files do not need to have the .asm extension (anything else will display a warning).
    - directories will be searched for .asm files.

<p align="right">(<a href="#top">back to top</a>)</p>

## Examples

- e.g.:
    - ```python ./ass.py ./add/ ./max/ ./pong/ ./rect/```
    - ```python3 ./ass.py ./add/ ./max/ ./pong/ ./rect/```

```bash
   INFO: Searching directory '.\add\' for .asm files.
   INFO: File '.\add\Add.asm' collected.
   INFO: Searching directory '.\max\' for .asm files.
   INFO: File '.\max\Max.asm' collected.
   INFO: File '.\max\MaxL.asm' collected.
   INFO: Searching directory '.\pong\' for .asm files.
   INFO: File '.\pong\Pong.asm' collected.
   INFO: File '.\pong\PongL.asm' collected.
   INFO: Searching directory '.\rect\' for .asm files.
   INFO: File '.\rect\Rect.asm' collected.
   INFO: File '.\rect\RectL.asm' collected.

   INFO: Assembling '.\pong\PongL.asm' to '.\pong\PongL.hack'
   INFO: Successfully assembled '.\pong\PongL.asm' to '.\pong\PongL.hack'

   INFO: Assembling '.\pong\Pong.asm' to '.\pong\Pong.hack'
   INFO: Successfully assembled '.\pong\Pong.asm' to '.\pong\Pong.hack'

   INFO: Assembling '.\rect\Rect.asm' to '.\rect\Rect.hack'
   INFO: Successfully assembled '.\rect\Rect.asm' to '.\rect\Rect.hack'

   INFO: Assembling '.\max\Max.asm' to '.\max\Max.hack'
   INFO: Successfully assembled '.\max\Max.asm' to '.\max\Max.hack'

   INFO: Assembling '.\max\MaxL.asm' to '.\max\MaxL.hack'
   INFO: Successfully assembled '.\max\MaxL.asm' to '.\max\MaxL.hack'

   INFO: Assembling '.\add\Add.asm' to '.\add\Add.hack'
   INFO: Successfully assembled '.\add\Add.asm' to '.\add\Add.hack'

   INFO: Assembling '.\rect\RectL.asm' to '.\rect\RectL.hack'
   INFO: Successfully assembled '.\rect\RectL.asm' to '.\rect\RectL.hack'
```

semantic errors are being checked and reported by providing their line number and line content.



```
   INFO: Assembling './max/MaxL.asm' to './max/MaxL.hack'
  ERROR: Invalid jump 'JMP?' in line 18: 0;JMP?

   INFO: Assembling './rect/Rect.asm' to './rect/Rect.hack'
  ERROR: Invalid comp 'X' in line 19: D=X

   INFO: Assembling './max/Max.asm' to './max/Max.hack'
  ERROR: Invalid label format in line 22: (ITSR0

   INFO: Assembling './add/Add.asm' to './add/Add.hack'
WARNING: Address '999999999' exceeds 15 bits in line 8: @999999999
   INFO: Successfully assembled './add/Add.asm' to './add/Add.hack'
```

<p align="right">(<a href="#top">back to top</a>)</p>

## Contact

> **SilenZcience** <br/>
[![GitHub-SilenZcience][GitHub-SilenZcience]](https://github.com/SilenZcience)

[GitHub-SilenZcience]: https://img.shields.io/badge/GitHub-SilenZcience-orange

[OS-Windows]: https://img.shields.io/badge/os-windows-green
[OS-Linux]: https://img.shields.io/badge/os-linux-green
[OS-MacOS]: https://img.shields.io/badge/os-macOS-green
