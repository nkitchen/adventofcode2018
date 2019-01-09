#!/usr/bin/env python3

import fileinput
import re
from collections import namedtuple

Nanobot = namedtuple('Nanobot', 'pos signalRadius')

nanobots = []

for line in fileinput.input():
    m = re.search(r"pos=<(-?\d+,-?\d+,-?\d+)>, r=(\d+)", line)
    if m:
        pos = [int(n) for n in m.group(1).split(",")]
        r = int(m.group(2))
        nanobots.append(Nanobot(pos, r))

strongest = max(nanobots, key=lambda nb: nb.signalRadius)

n = 0
for j in range(0, len(nanobots)):
    p = nanobots[j].pos
    d = (abs(p[0] - strongest.pos[0]) +
         abs(p[1] - strongest.pos[1]) +
         abs(p[2] - strongest.pos[2]))
    if d <= strongest.signalRadius:
        n += 1
print(n)
