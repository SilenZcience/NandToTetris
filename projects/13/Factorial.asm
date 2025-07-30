


@500
D=M
@k
M=D
@result
M=1

@mula
M=0
@mulb
M=0
@mulresult
M=0

(FACLOOP)

@k
D=M-1

@END
D;JEQ

@k
D=M
@mula
M=D

@result
D=M
@mulb
M=D

@mulresult
M=0

@MULTLOOP
0;JMP

(MULTBACK)

@mulresult
D=M
@result
M=D

@k
M=M-1

@FACLOOP
0;JMP

(MULTLOOP)

@mula
MD=M-1

@MULTBACK
D;JLT

@mulb
D=M
@mulresult
M=M+D

@MULTLOOP
0;JMP

(END)

@result
D=M
@501
M=D

(HALT)
@HALT
0;JMP
