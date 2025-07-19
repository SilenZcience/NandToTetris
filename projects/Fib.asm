
    @501
    M=0 // clean R2

    @i // create iterative 'variable'
    M=0

    @tmpa
    M=0 // temporary variable to hold R0 value
    @tmpb
    M=1 // temporary variable to hold R1 value

(LOOP) // add R0 to R2, R1 times

// -------------------------------------------------------------------
// check break condition:
    @502
    D=M

    @i
    M=M+1 // increment iterative 'variable'

    D=D-M // calculate difference
    @END
    D;JLT // break if iterative 'variable' exceeds R1
// -------------------------------------------------------------------

// -------------------------------------------------------------------
// repetitive addition (without use of the symbol table):

    @tmpa
    D=M

    @tmpb
    D=D+M

    @501
    M=D // get R0 value

    @tmpb
    D=M // get R1 value
    @tmpa
    M=D

    @501
    D=M // get R0 value
    @tmpb
    M=D
// -------------------------------------------------------------------

// loop back
    @LOOP
    0;JMP

(END)
// nothing to do here, sum is already accumulated in R2
