#!/usr/bin/env python3

import fileinput
import functools
import operator
from collections import namedtuple

Loc = namedtuple('Loc', 'row col')

class Unit():
    attackPower = 3

    def __init__(self, loc):
        self.loc = loc
        self.hp = 200

class Elf(Unit):
    def __str__(self):
        return "E"
class Goblin(Unit):
    def __str__(self):
        return "G"

Elf.enemyType = Goblin
Goblin.enemyType = Elf

grid = []
units = []
for i, line in enumerate(fileinput.input()):
    row = list(line)
    for j, c in enumerate(row):
        if c in '#.':
            continue

        if c == 'G':
            g = Goblin(Loc(i, j))
            units.append(g)
            row[j] = g
        elif c == 'E':
            e = Elf(Loc(i, j))
            units.append(e)
            row[j] = e
        else:
            # Treat as annotation
            row = row[:j]
            break
    grid.append(row)

def display():
    def withHp(unit):
        return "{}({})".format(str(unit), unit.hp)

    for i, row in enumerate(grid):
        print(''.join(str(c) for c in row), end='')
        print('   ', end='')
        uu = [c for c in row if isinstance(c, Unit)]
        s = ', '.join(withHp(u) for u in uu)
        print(s)
    print()

def adjacent(loc):
    i, j = loc
    if i > 0:
        yield Loc(i - 1, j)
    if j > 0:
        yield Loc(i, j - 1)
    if j < len(grid[0]):
        yield Loc(i, j + 1)
    if i < len(grid):
        yield Loc(i + 1, j)

def findTargetsInRange(u):
    tir = []
    for loc in adjacent(u.loc):
        c = grid[loc.row][loc.col]
        if type(c) == u.enemyType:
            tir.append(c)
    return tir

CombatEnded = object()
UnableToMove = object()
Ready = object()

def move(u):
    targetsInRange = findTargetsInRange(u)
    if targetsInRange:
        return Ready, targetsInRange

    targets = [v for v in units if type(v) == u.enemyType]
    if len(targets) == 0:
        return CombatEnded, None

    inRangeOfTargets = set()
    for t in targets:
        for loc in adjacent(t.loc):
            if grid[loc.row][loc.col] == '.':
                inRangeOfTargets.add(loc)

    if not inRangeOfTargets:
        return UnableToMove, None

    # BFS

    visited = set([u.loc])
    # ply[d] is the locations visited in d steps
    ply = [set([u.loc])]
    reached = []
    while not reached:
        newPly = set()
        for loc in ply[-1]:
            for nbr in adjacent(loc):
                if nbr in visited:
                    continue
                if nbr in inRangeOfTargets:
                    reached.append(nbr)
                if grid[nbr.row][nbr.col] == '.':
                    newPly.add(nbr)
                    visited.add(nbr)
        if not newPly:
            break
        ply.append(newPly)

    if not reached:
        return UnableToMove, None

    reached.sort()
    goal = reached[0]

    # reached == inRangeOfTargets & ply[-1]
    # The elements of path[i] are the neighbors of path[i - 1]
    # that are also in the earlier ply (one step less distant).
    path = [set([goal])]
    for i in range(len(ply) - 2, 0, -1):
        a = set()
        for loc in path[-1]:
            a.update(adjacent(loc))
        path.append(a & ply[i])

    s = sorted(path[-1])
    dest = s[0]

    grid[u.loc.row][u.loc.col] = '.'
    u.loc = dest
    grid[dest.row][dest.col] = u

    return Ready, findTargetsInRange(u)

def run():
    fullRounds = 0
    while True:
        #display() # XXX
        units.sort(key=lambda u: u.loc)
        for i in range(len(units)):
            u = units[i]
            if not u:
                # Died before its turn
                continue

            code, targetsInRange = move(u)

            if code == CombatEnded:
                units[:] = filter(None, units)
                hp = sum(u.hp for u in units)
                return fullRounds * hp

            if code == UnableToMove or not targetsInRange:
                continue

            targetsInRange.sort(key=lambda u: (u.hp, u.loc))
            target = targetsInRange[0]
            target.hp -= u.attackPower
            if target.hp <= 0:
                # Died
                grid[target.loc.row][target.loc.col] = '.'
                j = units.index(target)
                units[j] = None

        units[:] = filter(None, units)
        fullRounds += 1
            
print(run())
