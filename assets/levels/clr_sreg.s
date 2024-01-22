.equ SREG ,0x3f
.org 0
main:		ldi r16,0
		out SREG,r16
mainloop:	rjmp mainloop