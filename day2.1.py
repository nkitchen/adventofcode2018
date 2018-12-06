#!/usr/bin/env python3

import collections
import fileinput

n2 = 0
n3 = 0
for line in fileinput.input():
    c = collections.Counter(line.strip())
    if 2 in c.values():
        n2 += 1
    if 3 in c.values():
        n3 += 1

print(n2 * n3)
