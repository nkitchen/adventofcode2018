#!/usr/bin/env python3

import numpy as np
import sys

serial = int(sys.argv[1])

n = 300

r = np.arange(1, n + 1)
x, y = np.meshgrid(r, r, sparse=True)

rackId = x + 10

power = rackId * y
power += serial
power *= rackId
power = power % 1000 // 100
power -= 5

groupPower = np.full((n, n, n), -1000000, dtype=power.dtype)
for m in range(1, 91):
    print('.', end='', file=sys.stderr, flush=True)
    s = np.arange(m)
    i, j = np.meshgrid(s, s, sparse=True)
    for u in range(0, n - (m - 1)):
        for v in range(0, n - (m - 1)):
            groupPower[m - 1][u][v] = power[i + u, j + v].sum()
print(file=sys.stderr)

a = groupPower.argmax(axis=None)
ii = np.unravel_index(a, groupPower.shape)

size = ii[0] + 1
yMax = y.flat[ii[1]]
xMax = x.flat[ii[2]]
print((xMax, yMax, size), groupPower.flat[a])
