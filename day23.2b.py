#!/usr/bin/env python3

import fileinput
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

pw = np.zeros((n, n))
for i in range(n):
    for j in range(i):
        if abs(pos[i] - pos[j]).sum() <= r[i] + r[j]:
            pw[i, j] = 1
            pw[j, i] = 1

"""
With my input, most bots have ranges intersecting with more than 900 others.
If I remove those that don't, do the remaining ones all intersect pairwise?
"""

many = pw.sum(axis=0) > 900
pwm = pw[np.ix_(many, many)]
res = ((pwm + np.identity(sum(many))) > 0).all()
print(res)

# Answer: yes
