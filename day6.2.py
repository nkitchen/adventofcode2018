#!/usr/bin/env python3

import fileinput
import re
import sys
from collections import namedtuple
from collections import Counter

Point = namedtuple('Point', 'x y')

distLimit = int(sys.argv[1])

points = []
for line in fileinput.input(files=sys.argv[2:]):
   m = re.match(r'(\d+), (\d+)$', line)
   if m:
      points.append(Point(int(m.group(1)), int(m.group(2))))

xMin = min(p.x for p in points)
yMin = min(p.y for p in points)
xMax = max(p.x for p in points)
yMax = max(p.y for p in points)

n = 0
for x in range(xMin, xMax + 1):
   for y in range(yMin, yMax + 1):
      d = 0
      for p in points:
         d += abs(x - p.x) + abs(y - p.y)
      if d < distLimit:
         n += 1

print(n)
