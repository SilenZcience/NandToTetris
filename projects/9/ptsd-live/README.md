
<div id="top"></div>

[![OS-Windows]][OS-Windows]
[![OS-Linux]][OS-Linux]
[![OS-MacOS]][OS-MacOS]

<br/>
<div align="center">
<h2 align="center">Nand2Tetris Project 9 - PTSD-Live</h2>
   <p align="center">
      PTSD-Live is a simple game inspired by <a href="https://www.shellshocklive.com/">ShellShock Live</a>, where players control tanks and engage in turn-based battles. Players can adjust their tank's angle and power to fire projectiles at opponents, aiming to hit them while avoiding incoming fire.
   </p>
</div>

<details>
   <summary>Table of Contents</summary>
   <ol>
      <li>
         <a href="#getting-started">Getting Started</a>
         <ul>
            <li><a href="#prerequisites">Prerequisites</a></li>
            <li><a href="#compilation">Compilation</a></li>
            <li><a href="#play">Play</a></li>
         </ul>
      </li>
      <li><a href="#documentation">Documentation</a></li>
         <ul>
            <li><a href="#controls">Controls</a></li>
            <li><a href="#weapons">Weapons</a></li>
            <li><a href="#levels">Levels</a></li>
            <li><a href="#highscore">Highscore</a></li>
            <li><a href="#cheating">Cheating</a></li>
         </ul>
      <li><a href="#contact">Contact</a></li>
   </ol>
</details>

<div id="getting-started"></div>

<h2>
	<a href="#">&#x200B;</a>
	<a href="#getting-started" title="Noto Emoji, licensed under CC BY 4.0">
		<img unselectable="on" pointer-events="none" src="https://fonts.gstatic.com/s/e/notoemoji/latest/1f680/512.gif" width="18" />
	</a>
	<b>Getting Started</b>
</h2>

<div id="prerequisites"></div>

<h3>
	<a href="#">&#x200B;</a>
	<a href="#prerequisites" title="Noto Emoji, licensed under CC BY 4.0">
		<img unselectable="on" pointer-events="none" src="https://fonts.gstatic.com/s/e/notoemoji/latest/270f_fe0f/512.gif" width="15" />
	</a>
	<b>Prerequisites</b>
</h3>

- you will need a JackCompiler
- you will need a VMEmulator

(both of which can be acquired from the official [Nand2Tetris](https://www.nand2tetris.org/course) course)

<div id="compilation"></div>

<h3>
	<a href="#">&#x200B;</a>
	<a href="#compilation" title="Noto Emoji, licensed under CC BY 4.0">
		<img unselectable="on" pointer-events="none" src="https://fonts.gstatic.com/s/e/notoemoji/latest/2699_fe0f/512.gif" width="15" />
	</a>
	<b>Compilation</b>
</h3>

In order to compile the given `.jack`-files to executable `.vm`-files, simply use the `JackCompiler` provided by the [Nand2Tetris](https://www.nand2tetris.org/course) course (or any other JackCompiler). Run the following command:

```console
JackCompiler <.../ptsd-live/src>
```

<div id="play"></div>

<h3>
	<a href="#">&#x200B;</a>
	<a href="#play" title="Noto Emoji, licensed under CC BY 4.0">
		<img unselectable="on" pointer-events="none" src="https://fonts.gstatic.com/s/e/notoemoji/latest/1f3af/512.gif" width="15" />
	</a>
	<b>Play</b>
</h3>

In order to play the game either load the `<.../ptsd-live/src` folder into the `VMEmulator` provided by the [Nand2Tetris](https://www.nand2tetris.org/course) course or simply use the [Nand-to-Browser](https://funkschy.github.io/nand-to-browser/) website to load all compiled `.vm` files.

<p align="right">(<a href="#top">back to top</a>)</p>

<div id="documentation"></div>

<h2>
	<a href="#">&#x200B;</a>
	<a href="#documentation" title="Noto Emoji, licensed under CC BY 4.0">
		<img unselectable="on" pointer-events="none" src="https://fonts.gstatic.com/s/e/notoemoji/latest/1f4a1/512.gif" width="18" />
	</a>
	<b>Documentation</b>
</h2>

The game is turn-based. the players turn ends after taking a shot at an enemy tank, after which all enemy tanks will execute their turn sequentially and it is once again the players turn.

<div id="controls"></div>

<h3>
	<a href="#">&#x200B;</a>
	<a href="#controls" title="Noto Emoji, licensed under CC BY 4.0">
		<img unselectable="on" pointer-events="none" src="https://fonts.gstatic.com/s/e/notoemoji/latest/1f916/512.gif" width="15" />
	</a>
	<b>Controls</b>
</h3>

- W/D - Key
    - to move horizontally (to the left or right)
    - this action will deplete fuel
    - fuel will automatically be restored each turn
    - without fuel the tank will not be able to move
- left/right - Arrow
    - to adjust the shooting angle in increments of 5°
    - the default shooting angle is 0° (looking up)
    - the angle can be adjusted to at most 100° to either side
- up/down - Arrow
    - to adjust the shooting strength in increments of 1.
    - the default shooting strength is 15.
    - the shooting strength can be adjusted between the values 9 and 25.
- SPACE - Key
    - to shoot your shot at an enemy tank
    - the shot is dependant on the shooting angle and shooting strenght
    - after shooting the players turn will end
- Q - Key
    - to cycle through weapon types
    - see <a href="#weapons">Weapons</a> for more information
- ESC - Key
    - to quit the game
    - the highscore will be lost

<div id="weapons"></div>

<h3>
	<a href="#">&#x200B;</a>
	<a href="#weapons" title="Noto Emoji, licensed under CC BY 4.0">
		<img unselectable="on" pointer-events="none" src="https://fonts.gstatic.com/s/e/notoemoji/latest/1f4a5/512.gif" width="15" />
	</a>
	<b>Weapons</b>
</h3>

Three different weapon types are available:

- Small
    - has a radius of 1 pixel and an impact radius of 2 pixel
    - dealing 80 damage
- Medium
    - has a radius of 2 pixel and an impact radius of 12 pixel
    - dealing 40 damage
- Large
    - has a radius of 3 pixel and an impact radius of 22 pixel
    - dealing 20 damage

<div id="levels"></div>

<h3>
	<a href="#">&#x200B;</a>
	<a href="#levels" title="Noto Emoji, licensed under CC BY 4.0">
		<img unselectable="on" pointer-events="none" src="https://fonts.gstatic.com/s/e/notoemoji/latest/1f3c1/512.gif" width="15" />
	</a>
	<b>Levels</b>
</h3>

The game currently consists of 10 default levels with progressive difficulty.

One additional bonus level (Level 11) can be played by beating all 10 default levels without getting destroyed once (good luck).

New levels can be added incredibly easy by adding to the `Levels.jack` file.
Simply add an if-statement to the `tankAmount`-function which returns the amount of tanks on the new level-map.
Define your level inside the `initLevel`-function by providing a new if-statement containing the height-values to design the map and add tanks to any position. The first tank in the alltanks-array will always be the player tank.

<div id="highscore"></div>

<h3>
	<a href="#">&#x200B;</a>
	<a href="#highscore" title="Noto Emoji, licensed under CC BY 4.0">
		<img unselectable="on" pointer-events="none" src="https://fonts.gstatic.com/s/e/notoemoji/latest/1f3c6/512.gif" width="15" />
	</a>
	<b>Highscore</b>
</h3>

For every point of damage you deal to an enemy tank your score will increment by 1.
For example a hit with a medium shot (dealing 40 damage) will increase your score by 40.
A direct hit (not hitting the ground directly next to an enemy) will multiply the added score with the factor 1,3.
For example a direct hit with a medium shot will not increment the score by 40, but 40 multiplied by 1,3, therefor increasing the score by 52 points.

Additionally you will get bonus points after each level if you clear a level with fewer shots.
If a level has 1 enemy, you will get bonus points if you need less than 4 shots (for 2 enemies less than 8 shots and so on).
If a level has 3 enemies (you need less than 12 shots) and you clear the level with only 9 shots the difference (12-9 = 3) will be multiplied by 15 (3*15 = 45) and added to the score.

<div id="cheating"></div>

<h3>
	<a href="#">&#x200B;</a>
	<a href="#cheating" title="Noto Emoji, licensed under CC BY 4.0">
		<img unselectable="on" pointer-events="none" src="https://fonts.gstatic.com/s/e/notoemoji/latest/1f6a9/512.gif" width="15" />
	</a>
	<b>Cheating</b>
</h3>

If you wish to play through all levels without fearing for death, the easiest way to cheat invulnerability is to change the `applyDamage`-function within the `Tank.jack`-file by changing the statement `if (destroyed) { return; }` to `if (destroyed | playerTank) { return; }`. (This of course is for developing and testing purposes only 😏).

You can also change the first `let level = 1;` line within the `Main.jack` file to start the game at a certain level.

(Cheating ain't difficult if you have the source code ... Don't be a B*tch 🙃).


<div id="contact"></div>

<h2>
	<a href="#">&#x200B;</a>
	<a href="#contact" title="Noto Emoji, licensed under CC BY 4.0">
		<img unselectable="on" pointer-events="none" src="https://fonts.gstatic.com/s/e/notoemoji/latest/1f4ab/512.gif" width="18" />
	</a>
	<b>Contact</b>
</h2>

> **SilenZcience** <br/>
[![GitHub-SilenZcience][GitHub-SilenZcience]](https://github.com/SilenZcience)

[GitHub-SilenZcience]: https://img.shields.io/badge/GitHub-SilenZcience-orange

[OS-Windows]: https://img.shields.io/badge/os-windows-green
[OS-Linux]: https://img.shields.io/badge/os-linux-green
[OS-MacOS]: https://img.shields.io/badge/os-macOS-green
