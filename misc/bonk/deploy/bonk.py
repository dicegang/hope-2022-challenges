#!/usr/bin/env python3
import string
code = input("Welcome to python! Enter your code: ")
allowed = set(string.ascii_lowercase+'()[]._'+string.digits)
if allowed | set(code) != allowed:
    raise Exception("bonk go to python jail")
compile(code, "", "eval")
print(code)
eval(code[0:-1:2], {"__builtins__": None})
