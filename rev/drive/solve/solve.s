; vim: ft=nasm
s:

%macro i_nop 0
    db 0x00
%endmacro
%define np i_nop

%macro i_halt 1
    db 0x01
    db %1
%endmacro
%define ht i_halt

; load <mem> <value>
%macro i_load 2
    db 0x10
    db %1
    db %2
%endmacro
%define ld i_load

; send <device> <mem>
%macro i_send 2
    db 0x20
    db %1
    db %2
%endmacro
%define sd i_send

; get <mem> <device>
%macro i_get 2
    db 0x21
    db %1
    db %2
%endmacro
%define gt i_get


; jlt <a>, <b>, <loc>
; a < b
%macro i_less 3
    db 0x50
    db %1
    db %2
    db (%3 >> 8) & 0xff
    db %3 & 0xff
%endmacro
%define jl i_less


; jle <a>, <b>, <loc>
; a <= b
%macro i_leq 3
    db 0x51
    db %1
    db %2
    db (%3 >> 8) & 0xff
    db %3 & 0xff
%endmacro
%define le i_leq

%define inp 0
%define disp 1
%define arith 2
%define tape 3

gt 0x00, inp
gt 0x01, inp
gt 0x02, inp
gt 0x03, inp

sd tape, 0x00
sd tape, 0x02
sd tape, 0x01
sd tape, 0x03
sd arith, 0x00
sd arith, 0x03
sd tape, 0x00
ld 0x00, 0x01
sd arith, 0x00
gt 0x00, tape
gt 0x03, arith
sd arith, 0x01
sd arith, 0x03
sd tape, 0x00
ld 0x00, 0x03
sd arith, 0x00
gt 0x00, tape
gt 0x03, arith
sd arith, 0x00
sd arith, 0x01
sd tape, 0x00
ld 0x00, 0x01
sd arith, 0x00
gt 0x00, tape
gt 0x00, arith
sd arith, 0x00
sd arith, 0x02
sd tape, 0x00
ld 0x00, 0x03
sd arith, 0x00
gt 0x00, tape
gt 0x02, arith
sd arith, 0x00
sd arith, 0x02
sd tape, 0x00
ld 0x00, 0x03
sd arith, 0x00
gt 0x00, tape
gt 0x00, arith
sd arith, 0x00
sd arith, 0x01
sd tape, 0x00
ld 0x00, 0x01
sd arith, 0x00
gt 0x00, tape
gt 0x01, arith
sd arith, 0x01
gt 0x01, tape
sd arith, 0x01
sd tape, 0x00
ld 0x00, 0x03
sd arith, 0x00
gt 0x00, tape
gt 0x01, arith
sd arith, 0x00
gt 0x00, tape
sd arith, 0x00
sd tape, 0x00
ld 0x00, 0x01
sd arith, 0x00
gt 0x00, tape
gt 0x00, arith
sd arith, 0x00
sd arith, 0x01
sd tape, 0x00
ld 0x00, 0x03
sd arith, 0x00
gt 0x00, tape
gt 0x00, arith
sd arith, 0x00
gt 0x00, tape
sd arith, 0x00
sd tape, 0x00
ld 0x00, 0x01
sd arith, 0x00
gt 0x00, tape
gt 0x00, arith
sd arith, 0x00
gt 0x00, tape
sd arith, 0x00
sd tape, 0x00
ld 0x00, 0x03
sd arith, 0x00
gt 0x00, tape
gt 0x00, arith
sd tape, 0x00
sd tape, 0x01
sd tape, 0x02
sd tape, 0x03
gt 0x01, tape
gt 0x02, tape
gt 0x03, tape
gt 0x00, tape
sd tape, 0x01
sd arith, 0x01
ld 0x01, 0x00
sd arith, 0x01
ld 0x01, 0x01
sd arith, 0x01
sd tape, 0x03
gt 0x01, tape
sd tape, 0x01
gt 0x01, arith
loop:
sd tape, 0x02
sd tape, 0x03
sd tape, 0x00
gt 0x03, tape
multip:
sd arith, 0x02
ld 0x02, 0x01
sd arith, 0x02
ld 0x02, 0x02
sd arith, 0x02
gt 0x02, arith
sd arith, 0x00
sd arith, 0x03
ld 0x00, 0x01
sd arith, 0x00
gt 0x00, arith
sd tape, 0x00
ld 0x00, 0x01
le 0x02, 0x00, leavemul - s
gt 0x00, tape
le 0x00, 0x00, multip - s
leavemul:
gt 0x00, tape
gt 0x03, tape
gt 0x02, tape
sd arith, 0x00
sd arith, 0x01
sd tape, 0x00
ld 0x00, 0x01
sd arith, 0x00
gt 0x00, tape
gt 0x00, arith
modulo:
jl 0x00, 0x03, leavemod - s
sd arith, 0x00
sd arith, 0x03
sd tape, 0x00
ld 0x00, 0x02
sd arith, 0x00
gt 0x00, tape
gt 0x00, arith
le 0x00, 0x00, modulo - s
leavemod:
gt 0x01, tape
sd arith, 0x01
ld 0x01, 0x01
sd arith, 0x01
ld 0x01, 0x02
sd arith, 0x01
gt 0x01, arith
sd tape, 0x02
ld 0x02, 0x00
le 0x01, 0x02, finish - s
gt 0x02, tape
sd arith, 0x02
ld 0x02, 0x00
sd arith, 0x02
ld 0x02, 0x01
sd arith, 0x02
gt 0x02, tape
sd tape, 0x02
sd tape, 0x01
sd tape, 0x02
gt 0x02, arith
gt 0x01, tape
le 0x03, 0x03, loop - s
finish: 
gt 0x02, tape
gt 0x01, tape
sd disp, 0x00
sd disp, 0x01
sd disp, 0x02
sd disp, 0x03
