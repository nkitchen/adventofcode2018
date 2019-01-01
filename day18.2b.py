#!/usr/bin/env python3

import fileinput

lines = list(fileinput.input())
m = len(lines)

# Last 28 values repeat

n = 1000000000

# value(n) == value(m - k) for which n % 28 == (m - k + 1) % 28

for k in range(m, m - 29, -1):
    if n % 28 == (k + 1) % 28:
        print(lines[k])
