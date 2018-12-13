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

groupPower = np.zeros((n - 2, n - 2), dtype=power.dtype)
s = np.arange(3)
i, j = np.meshgrid(s, s, sparse=True)
for u in range(0, n - 2):
    for v in range(0, n - 2):
        groupPower[u][v] = power[i + u, j + v].sum()

a = groupPower.argmax(axis=None)
row, col = np.unravel_index(a, groupPower.shape)

xMax = x.flat[col]
yMax = y.flat[row]
print((xMax, yMax), groupPower.flat[a])
