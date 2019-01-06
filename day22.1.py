#!/usr/bin/env python3

import fileinput
import numpy as np
import re

for line in fileinput.input():
    m = re.search(r'depth: (\d+)', line)
    if m:
        depth = int(m.group(1))

    m = re.search(r'target: (\d+),(\d+)', line)
    if m:
        target = (int(m.group(1)), int(m.group(2)))

xMax = target[0]
yMax = target[1]
x, y = np.meshgrid(np.arange(0, xMax + 1),
                   np.arange(0, yMax + 1),
                   sparse=True)

geoIndex = np.zeros((xMax + 1, yMax + 1), dtype=int)
geoIndex[..., 0] = x * 16807
geoIndex[0, ...] = (y * 48271).reshape((1, yMax + 1))

erosion = (geoIndex + depth) % 20183

for x in range(1, xMax + 1):
    for y in range(1, yMax + 1):
        geoIndex[x, y] = erosion[x - 1, y] * erosion[x, y - 1]
        erosion[x, y] = (geoIndex[x, y] + depth) % 20183

geoIndex[target] = 0
erosion[target] = (geoIndex[target] + depth) % 20183

regType = erosion % 3

def display():
    for y in range(0, yMax + 1):
        for x in range(0, xMax + 1):
            if (x, y) == target:
                c = "T"
            else:
                c = ".=|"[regType[x, y]]
            print(c, end="")
        print()

print(regType.sum())
