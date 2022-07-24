import json
with open('constraints.json') as f:
  constraints = json.load(f)
flag = open('flag.txt', 'rb').read().strip()

arith = {
  'add': lambda a, b: flag[a] + flag[b],
  'sub': lambda a, b: flag[a] - flag[b],
  'xor': lambda a, b: flag[a] ^ flag[b],
}

syms = {
  'add': '+',
  'sub': '-',
  'xor': '^',
  'ne': '!=',
  'eq': '==',
  'ge': '>=',
  'le': '<=',
}

def gen():
  yield f'strlen(flag) == {len(flag)}'
  for i in range(len(flag)):
    yield f'flag[{i}] > 0x20'
    yield f'flag[{i}] < 0x7f'
  for i, c in enumerate(flag[:len('hope')]):
    yield f'flag[{i}] == {c}'
  for a, b, op in constraints:
    y = f'flag[{a}] {syms[op]} flag[{b}]'
    if op in arith:
      y = f'({y}) == {arith[op](a, b)}'
    yield y

with open('zzz.c.j2') as f:
  tmp = f.read()

deet = tmp.replace('{{ conditions }}', ' && '.join(f'({x})' for x in gen()))

with open('zzz.c', 'w') as f:
  f.write(deet)
