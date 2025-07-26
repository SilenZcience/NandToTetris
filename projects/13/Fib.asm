// k-te fib zahl, k in addresse R3
// ergebnis in R2

@R2
M=0

@fib1
M=0
@fib2
M=1

(loop)

@R3
D=M
M=M-1
@end
D;JLE

@fib1
D=M
@fib2
D=D+M
@R2
M=D

@fib2
D=M
@fib1
M=D

@R2
D=M
@fib2
M=D

@loop
0;JMP

(end)
