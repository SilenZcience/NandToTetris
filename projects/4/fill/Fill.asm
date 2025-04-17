// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed,
// the screen should be cleared.

// initiate the @pos symbol to the screen base address minus 1
// (because we will increment it before using it every iteration)
    @SCREEN
    D=A
    @pos
    M=D-1

(AWAIT)

    @KBD
    D=M
    @BLACKEN // if a key is pressed, go to BLACKEN
    D;JGT
    @CLEAR   // else go to CLEAR
    0;JMP

(BLACKEN)

    @24575 // == 16384[SCREEN BASE ADDRESS] + (256[ROWS] * 512[COLS]) / 16 - 1 == the max address of the screen
    D=A
    @pos
    D=D-M
    @AWAIT
    D;JLE // == JEQ, if the screen is fully black (we reached the last screen address), go back to AWAIT

    // first increment, then write the pixel

    @pos
    M=M+1 // increment position to the next pixel

    A=M
    M=-1  // color the pixel black

    // continue blackening the screen because it is more efficient and the task did not specify interactivity during screen changes
    // instead we could jump back to AWAIT and slowly lower or raise the black 'curtain'
    @BLACKEN
    0;JMP

(CLEAR)

    @SCREEN
    D=A
    @pos
    D=M-D
    @AWAIT
    D;JLT  // if the screen is fully cleared (we exceeded the first screen address), go back to AWAIT

    // first write the pixel, then decrement

    @pos
    A=M
    M=0   // color the pixel white

    @pos
    M=M-1 // decrement position to the previous pixel

    // continue clearing the screen because it is more efficient and the task did not specify interactivity during screen changes
    // instead we could jump back to AWAIT and slowly lower or raise the black 'curtain'
    @CLEAR
    0;JMP
