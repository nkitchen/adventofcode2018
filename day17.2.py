#!/usr/bin/env python3

import copy
import fileinput
import re
from collections import defaultdict
from collections import namedtuple
from collections import ChainMap

Loc = namedtuple('Loc', 'x y')

cell = defaultdict(lambda: '.')

cell[Loc(500, 0)] = '+'

for line in fileinput.input():
    m = re.search(r"x=(\d+), y=(\d+)[.][.](\d+)", line)
    if m:
        x = int(m.group(1))
        y1 = int(m.group(2))
        y2 = int(m.group(3))
        for y in range(y1, y2 + 1):
            cell[Loc(x, y)] = '#'
        continue

    m = re.search(r"y=(\d+), x=(\d+)[.][.](\d+)", line)
    if m:
        y = int(m.group(1))
        x1 = int(m.group(2))
        x2 = int(m.group(3))
        for x in range(x1, x2 + 1):
            cell[Loc(x, y)] = '#'
        continue

yMin = min(loc.y for loc, v in cell.items() if v == '#')
yMax = max(loc.y for loc, v in cell.items() if v == '#')

def display():
    xMin = min(x for x, y in cell)
    xMax = max(x for x, y in cell)

    dcell = ChainMap({}, cell)
    for loc in q:
        dcell[loc] = 'Q'

    k = len(str(yMax))
    for y in range(yMin, yMax + 1):
        print(str(y).rjust(k),
              ''.join(dcell[Loc(x, y)] for x in range(xMin, xMax + 1)))
    print()

q = [Loc(500, 1)]

def assertCell(where, what):
    if cell[where] in what:
        return

    cell[where] = 'X'
    display()
    assert False
    import pdb; pdb.set_trace()

while q:
    #if Loc(674, 1913) in q:
    #    display()

    loc = q.pop()

    if cell[loc] in '~#':
        continue

    cell[loc] = '|'
    below = Loc(loc.x, loc.y + 1)
    if below.y > yMax:
        continue

    if cell[below] == '.':
        q.append(below)
        continue

    if cell[below] == '|':
        # Already reached
        continue

    if cell[below] in '#~':
        # Pooling
        xMin = loc.x
        leftWall = False
        while True:
            left = Loc(xMin - 1, loc.y)
            if cell[left] == '#':
                leftWall = True
                break
            assertCell(left, '.|')

            xMin -= 1

            belowLeft = Loc(xMin, loc.y + 1)
            if cell[belowLeft] in '.|':
                q.append(Loc(xMin, loc.y + 1))
                break

            assertCell(belowLeft, '#~')

        xMax = loc.x
        rightWall = False
        while True:
            if cell[Loc(xMax + 1, loc.y)] == '#':
                rightWall = True
                break
            assertCell(Loc(xMax + 1, loc.y), '.|')

            xMax += 1

            if cell[Loc(xMax, loc.y + 1)] in '.|':
                q.append(Loc(xMax, loc.y + 1))
                break

            assertCell(Loc(xMax, loc.y + 1), '#~')

        if leftWall and rightWall:
            for x in range(xMin, xMax + 1):
                cell[Loc(x, loc.y)] = '~'
            q.append(Loc(loc.x, loc.y - 1))
        else:
            for x in range(xMin, xMax + 1):
                cell[Loc(x, loc.y)] = '|'

n = 0
for loc in cell:
    if yMin <= loc.y <= yMax and cell[loc] in '~':
        n += 1
print(n)
# vim: set shiftwidth=4 :
