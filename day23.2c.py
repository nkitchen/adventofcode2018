#!/usr/bin/env python3

import fileinput
import itertools
import numpy as np
import re

"""
The range of each nanobot is an octahedron enclosed by four pairs of
sandwiching planes:

    -r_i <= x - a_i + y - b_i + z - c_i <= r_i
    -r_i <= x - a_i + y - b_i - z + c_i <= r_i
    -r_i <= x - a_i - y + b_i + z - c_i <= r_i
    -r_i <= x - a_i - y + b_i - z + c_i <= r_i

or:

    -r_i + a_i + b_i + c_i <= x + y + z <= r_i + a_i + b_i + c_i
    -r_i + a_i + b_i - c_i <= x + y - z <= r_i + a_i + b_i - c_i
    -r_i + a_i - b_i + c_i <= x - y + z <= r_i + a_i - b_i + c_i
    -r_i + a_i - b_i - c_i <= x - y - z <= r_i + a_i - b_i - c_i

The intersection of two octahedra is not necessarily an octahedron,
but because the sandwiching planes for a given set of x-y-z signs
are parallel, it is also defined by four pairs of planes:

    max(-r_i + a_i + b_i + c_i, -r_j + a_j + b_j + c_j)
        <= x + y + z <=
            min(r_i + a_i + b_i + c_i, r_j + a_j + b_j + c_j)
    etc.

Thus we can represent the intersection of any number of ranges
with 4 lower bounds and 4 upper bounds.
"""

pos = []
r = []

for line in fileinput.input():
    m = re.search(r"pos=<(-?\d+,-?\d+,-?\d+)>, r=(\d+)", line)
    if m:
        pos.append([int(n) for n in m.group(1).split(",")])
        r.append(int(m.group(2)))

n = len(pos)

pos = np.array(pos) # (n, 3)
r = np.array(r)

pw = np.zeros((n))
for i in range(n):
    for j in range(i):
        if abs(pos[i] - pos[j]).sum() <= r[i] + r[j]:
            pw[i] += 1
            pw[j] += 1

many = pw > (n / 2)
m = many.sum()

pos = pos[many]
r = r[many]

signs = np.array([[1,  1,  1],
                  [1,  1, -1],
                  [1, -1,  1],
                  [1, -1, -1]])

# a[i]: lower bounds for nanobot i
# b[i]: upper bounds
offset = pos @ signs.T
a = offset - r[:, None]
b = offset + r[:, None]

# Intersection bounds
c = a.max(axis=0)
d = b.min(axis=0)
assert (c <= d).all()

print(c)
print(d)

# Find corners by solving triples of bounds.
best = np.full(3, d.max())
cd = np.vstack((c, d))
for i in range(4):
    # i is the pair of bounds omitted, leaving the other three.
    ii = np.arange(4) != i
    coeffs = np.mat(signs[ii])
    icoeffs = coeffs ** -1

    # Each combination of lower/upper
    for jj in itertools.product([0, 1], repeat=3):
        jj = np.array(jj)
        icept = cd[jj, ii]
        sol = np.array(icoeffs @ icept).reshape(best.shape)
        e = signs @ sol
        if (c <= e).all() and (e <= d).all():
            print(np.int64(signs @ sol), sol, abs(sol).sum())
            if abs(sol).sum() < abs(best).sum():
                best = sol

if not (np.floor(best) == best).all():
    bestdist = abs(best).sum() + 4
    fc = np.vstack((np.floor(best), np.ceil(best)))
    for ii in itertools.product([0, 1], repeat=3):
        ii = np.array(ii)
        p = fc[ii, np.arange(3)]
        e = signs @ p
        if ((c <= e).all() and (e <= d).all() and
            abs(e).sum() < bestdist):
            best = e
            bestdist = abs(e).sum()

print(best, abs(best.sum()))

# vim: set shiftwidth=4 :
