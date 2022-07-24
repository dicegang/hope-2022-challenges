from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

with open('privatekey.pem','rb') as f:
	key = RSA.import_key(f.read())

with open("encrypted.bin", "rb") as f:
	enc = f.read()

cipher_rsa = PKCS1_OAEP.new(key)
flag = cipher_rsa.decrypt(enc)

print(flag.decode())
