

// multiply R0 and R1 into R2

@R2
M=0

(LOOP)

@R0
D=M
M=M-1
@END
D;JLE

@R1
D=M
@R2
M=D+M

@LOOP
0;JMP

(END)
@END
0;JMP
