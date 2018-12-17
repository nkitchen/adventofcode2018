#!/usr/bin/env python3

import fileinput
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

offset = 0
for g in range(20):
    t = []
    for k in range(4, 0, -1):
        nh = '.' * k + s[:5 - k]
        t.append(rules[nh])
    for i in range(2, len(s) - 2):
        nh = s[i-2:i+3]
        assert len(nh) == 5
        t.append(rules[nh])
    for k in range(1, 5):
        nh = s[-(5 - k):] + '.' * k
        t.append(rules[nh])

    t = ''.join(t)
    offset -= 2

    s = t

n = 0
for i, c in enumerate(s):
    if s[i] == '#':
        n += i + offset
print(n)
