#!/usr/bin/env python3

import fileinput

points = []

for line in fileinput.input():
    p = map(int, line.strip().split(","))
    points.append(tuple(p))


rep = {}

def findRep(p):
    r = rep.get(p, p)
    if r == p:
        return r

    r = findRep(r)
    rep[p] = r
    return r

def l1Dist(p, q):
    return sum(abs(a - b) for a, b in zip(p, q))

for i, p in enumerate(points):
    for j in range(i):
        q = points[j]
        if l1Dist(p, q) <= 3:
            r = findRep(p)
            rep[r] = findRep(q)

for p in points:
    findRep(p)

constellation = {}
for p in points:
    r = findRep(p)
    constellation.setdefault(r, []).append(p)

print(len(constellation))

# vim: set shiftwidth=4 :
