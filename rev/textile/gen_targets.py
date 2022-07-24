from utils import Rng

flag = r'''hope{/\_/\_/\-- Thanks for unraveling me! --/\_/\_/\ Hv$\;-*'^p5D%W3&}'''

if __name__ == '__main__':
    print(rf'\def\CFlagTargetLen{{"{len(flag):X}}}')

    targets_def = r'\def\CFlagTarget{'
    rng = Rng()
    uncovered_chars = {i for i in range(len(flag))}
    while uncovered_chars:
        idx = rng.get() % len(flag)
        addend = rng.get() % 0x100
        target = (ord(flag[idx]) + addend) % 0x100
        targets_def += f'{{"{target:02X}}}'
        uncovered_chars.discard(idx)
    targets_def += '}'
    print(targets_def)
