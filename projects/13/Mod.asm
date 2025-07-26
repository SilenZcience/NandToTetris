// R3 = R1 % R2

@R3
M=0


(loop)

@R2
D=M
@R1
MD=M-D

@end
D;JLT


@loop
0;JMP

(end)

@R2
D=M
@R1
D=D+M
@R3
M=D


(halt)
@halt
0;JMP
