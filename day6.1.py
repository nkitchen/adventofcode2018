#!/usr/bin/env python3

import fileinput
import re
from collections import namedtuple
from collections import Counter

Point = namedtuple('Point', 'x y')

points = []
for line in fileinput.input():
   m = re.match(r'(\d+), (\d+)$', line)
   if m:
      points.append(Point(int(m.group(1)), int(m.group(2))))

# A point is closest to an infinite number of points in an orthogonal
# direction unless there is another point in the cone extending in that
# direction.  For example, in the diagram below, the points with stars
# are in the cone from A for the positive x direction.  A point in that
# cone bounds the number of points in the cone closest to A.
#
# ....*   ....b
# ...**   ...bb
# ..***   ..abb
# .****   .aabb
# A****   Aaabb
# .****   .abbb
# ..***   ..bBb
# ...**   ...bb
# ....*   ....b
#
# The points whose total closest area is finite are the ones that have
# other points in their cones in all four directions.

conesOccupied = {}
for p in points:
   for q in points:
      if p == q:
         continue
      dx = q.x - p.x
      dy = q.y - p.y
      if dx < 0 and abs(dx) >= abs(dy):
         conesOccupied.setdefault(p, set()).add('-x')
      if dx > 0 and abs(dx) >= abs(dy):
         conesOccupied.setdefault(p, set()).add('+x')
      if dy < 0 and abs(dy) >= abs(dx):
         conesOccupied.setdefault(p, set()).add('-y')
      if dy > 0 and abs(dy) >= abs(dx):
         conesOccupied.setdefault(p, set()).add('+y')
boundedPoints = set(p for p in conesOccupied
                    if len(conesOccupied[p]) == 4)

# Breadth-first expansion from each point
closestSrc = {}
Multiple = object()

frontier = {}
for p in points:
   closestSrc[p] = p
   frontier[p] = set([p])

while True:
   expansionSrc = {}
   for src in points:
      for f in frontier.get(src, []):
         neighbors = [
            Point(f.x - 1, f.y),
            Point(f.x + 1, f.y),
            Point(f.x, f.y - 1),
            Point(f.x, f.y + 1),
         ]
         for nbr in neighbors:
            if nbr in closestSrc:
               # Reached with a lower distance
               pass
            elif nbr not in expansionSrc:
               # First time reached
               expansionSrc[nbr] = src
            elif expansionSrc.get(nbr) == src:
               # Reached from the same source with the same distance
               pass
            else:
               # Reached from another source with the same distance
               expansionSrc[nbr] = Multiple

   boundedGrew = False
   frontier = {}
   for p, src in expansionSrc.items():
      closestSrc[p] = src
      if src == Multiple:
         continue
      frontier.setdefault(src, set()).add(p)
      if src in boundedPoints:
         boundedGrew = True

   if not boundedGrew:
      break

c = Counter()
for p, src in closestSrc.items():
   if src != Multiple and src in boundedPoints:
      c[src] += 1

for _, n in c.most_common(1):
   print(n)
