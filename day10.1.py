#!/usr/bin/env python3

import fileinput
import re
from collections import namedtuple

P = namedtuple('P', 'x y')

pos = []
vel = []
for line in fileinput.input():
    m = re.search(r'position=< *(-?\d+), *(-?\d+)> velocity=< *(-?\d+), *(-?\d+)>', line)
    if not m:
        continue
    x = int(m.group(1))
    y = int(m.group(2))
    vx = int(m.group(3))
    vy = int(m.group(4))
    pos.append(P(x, y))
    vel.append(P(vx, vy))

def display():
    xMin = min(p.x for p in pos)
    xMax = max(p.x for p in pos)
    yMin = min(p.y for p in pos)
    yMax = max(p.y for p in pos)

    m = xMax - xMin + 1
    n = yMax - yMin + 1
    grid = [['.' for _ in range(m)]
            for _ in range(n)]

    for p in pos:
        i = p.x - xMin
        j = p.y - yMin
        try:
           grid[j][i] = '#'
        except IndexError:
           import pdb; pdb.set_trace()

    for row in grid:
        print(''.join(row))

def advance():
    global pos

    posNew = []
    for p, v in zip(pos, vel):
        x = p.x + v.x
        y = p.y + v.y
        posNew.append(P(x, y))
    pos = posNew

t = 0
tMax = None
while True:
    if (max(p.x for p in pos) - min(p.x for p in pos) < 200 and
        max(p.y for p in pos) - min(p.y for p in pos) < 200):
        print(t)
        display()
        print()

        if tMax is None:
            tMax = t + 100
        elif t > tMax:
            break
    advance()
    t += 1
