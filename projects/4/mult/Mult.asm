// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
// The algorithm is based on repetitive addition.

    @2
    M=0 // clean R2

    @i // create iterative 'variable'
    M=0

(LOOP) // add R0 to R2, R1 times

// -------------------------------------------------------------------
// check break condition:
    @1
    D=M

    @i
    M=M+1 // increment iterative 'variable'

    D=D-M // calculate difference
    @END
    D;JLT // break if iterative 'variable' exceeds R1
// -------------------------------------------------------------------

// -------------------------------------------------------------------
// repetitive addition (without use of the symbol table):
    @0
    D=M // get R0 value

    @2
    M=D+M // simply accumulate the value of R0 in R2 directly
// -------------------------------------------------------------------

// loop back
    @LOOP
    0;JMP

(END)
// nothing to do here, sum is already accumulated in R2
