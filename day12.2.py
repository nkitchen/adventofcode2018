#!/usr/bin/env python3

import fileinput
import itertools
import re
from collections import defaultdict

rules = defaultdict(lambda: '.')

for line in fileinput.input():
    m = re.match(r'initial state: ([#.]+)', line)
    if m:
        s = m.group(1)
        continue

    m = re.match(r'([#.]+) => ([#.])', line)
    if m:
        rules[m.group(1)] = m.group(2)
        continue

# No expansion on left
for r in itertools.product(*('.#' * 3)):
    assert rules['..' + ''.join(r)] == '.'

offset = -2
s = ".." + s

def advance(s):
    t = []
    t.append(rules['..' + s[:3]])
    t.append(rules['.' + s[:4]])
    for i in range(0, len(s) - 4):
        nh = s[i:i + 5]
        assert len(nh) == 5
        t.append(rules[nh])
    for k in range(1, 5):
        nh = s[-(5 - k):] + '.' * k
        t.append(rules[nh])

    t = ''.join(t).rstrip('.')
    return t

def value(s):
    n = 0
    for i, c in enumerate(s):
        if s[i] == '#':
            n += i + offset
    return n

# After some number of generations, the increment of the value per generation
# becomes constant.
N = 1000
for g in range(N):
    s = advance(s)

va = value(s)
s = advance(s)
vb = value(s)

d = vb - va
print((50 * 1000 ** 3 - N) * d + va)
