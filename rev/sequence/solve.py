from pwn import args, remote

host = args.HOST or 'localhost'
port = args.PORT or 31973

r = remote(host, port)
r.sendline(b'12 11 8 15 4 3')
r.stream()
