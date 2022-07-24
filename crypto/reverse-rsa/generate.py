from Crypto.PublicKey import RSA

with open('flag.txt','rb') as f:
	flag = f.read()

key = RSA.generate(2048)

N = key.n
p = key.p
q = key.q
e = key.e
d = key.d

m = int.from_bytes(flag, 'little')
c = pow(m, e, N)

with open("ciphertext.txt", "w") as f:
	f.write(str(c))

m2 = pow(c, d, N)
m2 = int.to_bytes(m2, 256, 'little')
print(m2.decode().strip())
