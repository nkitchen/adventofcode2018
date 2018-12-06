#!/usr/bin/env python3

import bisect
import collections
import fileinput
import re

Claim = collections.namedtuple('Claim', 'id x y w h')

def newClaim(line):
    fields = re.findall(r'\d+', line)
    nums = list(map(int, fields))
    return Claim(*nums)

claims = [newClaim(line) for line in fileinput.input()]

# Instead of keeping a grid of each square inch of the fabric,
# we keep a grid where each cell is a subrectangle between two
# edge coordinates of some claims.
xEdges = set()
yEdges = set()
for cl in claims:
    xEdges.add(cl.x)
    xEdges.add(cl.x + cl.w)
    yEdges.add(cl.y)
    yEdges.add(cl.y + cl.h)

xEdges = sorted(xEdges)
yEdges = sorted(yEdges)

claimCounts = [[0] * (len(yEdges) - 1)
               for _ in range(len(xEdges) - 1)]
for cl in claims:
    iLo = bisect.bisect_left(xEdges, cl.x)
    iHi = bisect.bisect_left(xEdges, cl.x + cl.w)
    assert xEdges[iLo] == cl.x
    assert xEdges[iHi] == cl.x + cl.w

    jLo = bisect.bisect_left(yEdges, cl.y)
    jHi = bisect.bisect_left(yEdges, cl.y + cl.h)
    assert yEdges[jLo] == cl.y
    assert yEdges[jHi] == cl.y + cl.h

    for i in range(iLo, iHi):
        for j in range(jLo, jHi):
            claimCounts[i][j] += 1

def intact(cl):
    iLo = bisect.bisect_left(xEdges, cl.x)
    iHi = bisect.bisect_left(xEdges, cl.x + cl.w)

    jLo = bisect.bisect_left(yEdges, cl.y)
    jHi = bisect.bisect_left(yEdges, cl.y + cl.h)

    for i in range(iLo, iHi):
        for j in range(jLo, jHi):
            if claimCounts[i][j] > 1:
                return False

    return True

for cl in claims:
    if intact(cl):
        print(cl)
