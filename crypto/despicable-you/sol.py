def xor(s1,s2):
    a = ''
    for i,j in zip(s1,s2):
        a += chr(ord(i)^ord(j))
    return a

def rekey(key):
    k = ""
    for i,c in enumerate(key):
        if i == len(key)-1:
            k += c
            k += chr(ord(c)^ord(key[0]))
        else:
            k += c
            k += chr(ord(c)^ord(key[i+1]))
    key = k

f = open('output.txt').read()
chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
for j in chars:
    for l in chars:
        key = xor('hope{'+j+l+'y', f[0:8])
        i = 0
        pt = ''
        while i < len(f):
            pt += xor(f[i:i+len(key)],key)
            i += len(key)
            rekey(key)
        print(j+l)
        print(pt)
