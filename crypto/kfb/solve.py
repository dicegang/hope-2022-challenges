from itertools import cycle, islice

from Crypto.Util.Padding import unpad
from Crypto.Util.strxor import strxor
from pwn import args, remote

host = args.HOST or 'localhost'
port = args.PORT or 31968

r = remote(host, port)

def get_output():
  r.recvuntil(b'> ')
  return bytes.fromhex(r.recvline().strip().decode())

def encrypt(ct):
  r.sendline(ct.hex().encode())
  r.recvuntil(b'')
  return get_output()

enc = get_output()
bit = encrypt(b'\0'*16)[:16]
bit = bytes(islice(cycle(bit), len(enc)))
flag = unpad(strxor(enc, bit), 16)
print(flag.decode())
