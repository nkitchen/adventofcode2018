#!/usr/bin/env python3

import fileinput
from collections import namedtuple

Loc = namedtuple('Loc', 'x y')

# Locations at even-x, even-y coordinates are rooms.
# Locations at odd-x, odd-y coordinates are walls at room corners.
# Locations are even-x, odd-y and odd-x, even-y are potential doors.

rooms = set()
doors = set()

def parseBranch(i):
    """Parses a subpattern A|B starting at pattern[i].

    It may be a degenerate case: simply A.

    Returns the index of the first unused character and a result tuple
    ('branch', (resA, resB, ...)).
    """

    branches = []
    while True:
        i, s = parseSeq(i)
        assert s is not None
        branches.append(s)
        if pattern[i] == '|':
            i += 1
        else:
            break
    if len(branches) == 1:
        return i, branches[0]
    else:
        return i, ('branch', tuple(branches))

def parseSeq(i):
    """Parses a subpattern AB starting at pattern[i].

    It may be a degenerate case: simply A, or even an empty sequence.

    Returns the index of the first unused character and a result tuple
    ('seq', (resA, resB, ...)).
    """

    seq = []

    while True:
        j = i
        while pattern[j] in "NSEW":
            j += 1
        if j > i:
            seq.append(('lit', pattern[i:j]))
            i = j

        if pattern[i] == "(":
            i, b = parseBranch(i + 1)
            assert pattern[i] == ")"
            seq.append(b)
            i += 1

        if pattern[i] in ")|$":
            return i, ('seq', tuple(seq))

# Current location
rooms.add(Loc(0, 0))

def display():
    xMin = min(loc.x for loc in rooms)
    xMax = max(loc.x for loc in rooms)
    yMin = min(loc.y for loc in rooms)
    yMax = max(loc.y for loc in rooms)

    for y in range(yMin - 1, yMax + 2):
        for x in range(xMin - 1, xMax + 2):
            if (x, y) == (0, 0):
                c = 'X'
            elif Loc(x, y) in rooms:
                c = '.'
            elif Loc(x, y) in doors and x % 2 == 1:
                c = '|'
            elif Loc(x, y) in doors and y % 2 == 1:
                c = '-'
            else:
                c = '#'
            print(c, end='')
        print()

def explore(startRoom, pattern):
    """Finds rooms along the routes described by the parsed pattern
    and the doors traversed to reach them.
    Adds the locations of the doors and rooms found to the corresponding sets.
    Returns the set of rooms that are possible destinations of the route.
    """

    if pattern[0] == 'lit':
        cur = startRoom
        for c in pattern[1]:
            if c == "N":
                door = Loc(cur.x, cur.y - 1)
                cur = Loc(cur.x, cur.y - 2)
            elif c == "S":
                door = Loc(cur.x, cur.y + 1)
                cur = Loc(cur.x, cur.y + 2)
            elif c == "W":
                door = Loc(cur.x - 1, cur.y)
                cur = Loc(cur.x - 2, cur.y)
            elif c == "E":
                door = Loc(cur.x + 1, cur.y)
                cur = Loc(cur.x + 2, cur.y)
            doors.add(door)
            rooms.add(cur)

        return set([cur])

    elif pattern[0] == 'seq':
        cur = set()
        cur.add(startRoom)
        for sub in pattern[1]:
            subDests = set()
            for r in cur:
                subDests |= explore(r, sub)
            cur = subDests
        return cur

    else:
        assert pattern[0] == 'branch'

        dests = set()
        for sub in pattern[1]:
            dests |= explore(startRoom, sub)
        return dests

pattern = next(fileinput.input()).strip()

assert pattern.startswith('^')
assert pattern.endswith('$')

_, parsed = parseBranch(1)
explore(Loc(0, 0), parsed)

def neighbors(room):
    nd = Loc(room.x, room.y - 1)
    nr = Loc(room.x, room.y - 2)
    if nd in doors:
        yield nd, nr

    sd = Loc(room.x, room.y + 1)
    sr = Loc(room.x, room.y + 2)
    if sd in doors:
        yield sd, sr

    wd = Loc(room.x - 1, room.y)
    wr = Loc(room.x - 2, room.y)
    if wd in doors:
        yield wd, wr

    ed = Loc(room.x + 1, room.y)
    er = Loc(room.x + 2, room.y)
    if ed in doors:
        yield ed, er

def bfs():
    dist = {Loc(0, 0): 0}
    q = [Loc(0, 0)]

    while q:
        r = q.pop(0)
        for door, nbr in neighbors(r):
            if nbr in dist:
                continue

            dist[nbr] = dist[r] + 1
            q.append(nbr)

    return dist

dist = bfs()
print(sum(1 for d in dist.values() if d >= 1000))

# vim: set shiftwidth=4 :
