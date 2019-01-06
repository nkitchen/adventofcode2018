#!/usr/bin/env python3

import fileinput
import heapq
import re
from functools import lru_cache
from pprint import pprint

for line in fileinput.input():
    m = re.search(r'depth: (\d+)', line)
    if m:
        depth = int(m.group(1))

    m = re.search(r'target: (\d+),(\d+)', line)
    if m:
        target = (int(m.group(1)), int(m.group(2)))

xMax = target[0]
yMax = target[1]

@lru_cache(maxsize=None)
def geoIndex(x, y):
    if x == target[0] and y == target[1]:
        return 0
    if x == 0:
        return y * 48271
    if y == 0:
        return x * 16807

    return erosion(x - 1, y) * erosion(x, y - 1)

@lru_cache(maxsize=None)
def erosion(x, y):
    return (geoIndex(x, y) + depth) % 20183

ROCKY = 0
WET = 1
NARROW = 2

def regType(x, y):
    return erosion(x, y) % 3

def display():
    for y in range(0, target[1] + 1):
        for x in range(0, target[0] + 1):
            if (x, y) == target:
                c = "T"
            else:
                c = ".=|"[regType(x, y)]
            print(c, end="")
        print()
    print()

TORCH = 0
CLIMB_GEAR = 1
NEITHER = 2

compatibleTools = {
    ROCKY: [CLIMB_GEAR, TORCH],
    WET: [CLIMB_GEAR, NEITHER],
    NARROW: [TORCH, NEITHER],
}

def search():
    """A* search"""

    q = []

    def enqueue(x, y, tool, timeTo):
        heurTimeFrom = abs(x - target[0]) + abs(y - target[1])
        heapq.heappush(q, (timeTo + heurTimeFrom, x, y, tool, timeTo))

    enqueue(0, 0, TORCH, 0)
    visited = set()

    while q:
        #pprint(['q', q])
        t, x, y, tool, timeTo = heapq.heappop(q)
        if (x, y, tool) in visited:
            continue

        visited.add((x, y, tool))

        if x == target[0] and y == target[1] and tool == TORCH:
            return timeTo

        rtype = regType(x, y)

        for i in range(1, 3):
            otherTool = (tool + i) % 3
            if otherTool in compatibleTools[rtype]:
                enqueue(x, y, otherTool, timeTo + 7)

        nbrs = []
        if x > 0:
            nbrs.append((x - 1, y))
        nbrs.append((x + 1, y))
        if y > 0:
            nbrs.append((x, y - 1))
        nbrs.append((x, y + 1))

        for xn, yn in nbrs:
            rtn = regType(xn, yn)
            if tool in compatibleTools[rtn]:
                enqueue(xn, yn, tool, timeTo + 1)

print(search())

# vim: set shiftwidth=4 :
