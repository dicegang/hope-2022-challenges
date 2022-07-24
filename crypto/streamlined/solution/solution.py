import re
from tqdm import tqdm

with open('../stream_output.txt') as f:
    ciphertext_string = f.read()

ciphertext_bits = [int(i) for i in ciphertext_string]

N = len(ciphertext_bits)
key_length = N // 5

# make pairwise probability matrix
with open('texts/my-immortal.txt', 'rb') as f:
    text = f.read()

# my immortal is a little short
with open('texts/child-of-the-storm.txt', 'rb') as f:
    text += f.read()

frequencies = {}
for a, b in zip(text, text[1:]):
    if a not in frequencies:
        frequencies[a] = {}
    if b not in frequencies[a]:
        frequencies[a][b] = 0
    frequencies[a][b] += 1

probabilities = {}
for a, occurrences in frequencies.items():
    total = sum(occurrences.values())
    probabilities[a] = {}
    for b, count in occurrences.items():
        probabilities[a][b] = count / total

# iterate over matching-key sections
# use indices so we know when characters start and end
plaintext_bits = [0] * N

def write_bits(bits, start):
    for i in range(len(bits)):
        if i + start < N:
            plaintext_bits[i + start] = bits[i]

def pairwise_xor(a, b):
    return [a ^ b for a, b in zip(a, b)]

def bits(number):
    return [int(i) for i in f'{number:08b}']

def integer(bitarray):
    return int('0' + ''.join(map(str, bitarray)), 2)

def completed_group(start):
    # we want bytes that cross the starting edge
    # and end at start + 8
    nearest_start = start // 8 * 8 - 8
    nearest_end = nearest_start + 24

    # turn the range into three ints
    values = []
    for i in range(nearest_start, nearest_end, 8):
        values.append(integer(plaintext_bits[i:i + 8]))
    return values

first_key = pairwise_xor(ciphertext_bits, bits(ord(' ')) + bits(ord(' ')))
for i in range(0, N, key_length):
    ciphertext_window = ciphertext_bits[i:i + 16]
    plaintext = pairwise_xor(ciphertext_window, first_key)
    write_bits(plaintext, i)

for start in tqdm(range(16, key_length, 8)):
    previous_char = integer(plaintext_bits[start - 8:start])

    first_char = ciphertext_bits[start:start + 16]

    # go over possible pairs of next characters
    best = (0, [0] * 8)

    # for debugging purposes
    log = []

    # we look ahead by one for misalignment reasons
    for next_char in probabilities[previous_char]:
        for next_next_char in probabilities[next_char]:
            guess = bits(next_char) + bits(next_next_char)
            guess_key = pairwise_xor(first_char, guess)

            probability = 1
            for i in range(start, N // key_length * key_length, key_length):
                ciphertext_window = ciphertext_bits[i:i + 16]
                plaintext = pairwise_xor(ciphertext_window, guess_key)

                write_bits(plaintext, i)
                previous, current, next = completed_group(i)
                write_bits([0] * 16, i)

                # don't lose ALL resolution if the pair does not exist
                O = 1e-10
                probability *= probabilities.get(previous, {}).get(current, O)
                probability *= probabilities.get(current, {}).get(next, O)

            log.append((probability, chr(next_char), chr(next_next_char)))

            best = max(best, (probability, guess_key))

    # write the best guess
    probability, key = best
    for i in range(start, N, key_length):
        ciphertext_window = ciphertext_bits[i:i + 8]
        plaintext = pairwise_xor(ciphertext_window, key)
        write_bits(plaintext, i)

grouped = [integer(plaintext_bits[i:i + 8]) for i in range(0, N, 8)]
matches = re.findall('.*hope.(.+).$', ''.join(map(chr, grouped)))

assert len(matches) > 0

flag = matches[0]
print(f'hope{{{flag}}}')
