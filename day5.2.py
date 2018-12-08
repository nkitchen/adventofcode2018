#!/usr/bin/env python3

import fileinput
import pyllist
import re

s = next(fileinput.input()).strip()

def reacting(c, d):
    return c.lower() == d.lower() and c.islower() != d.islower()

units = set(c.lower() for c in s)

def reacted(s):
    # Ranges of indices where units have been destroyed
    destroyed = pyllist.dllist()

    i = 0
    while i < len(s) - 1:
        if reacting(s[i], s[i + 1]):
            n = destroyed.last
            if n and n.value.stop == i:
                r = n.value
                n.value = range(r.start, i + 2)
            else:
                destroyed.append(range(i, i + 2))

            i += 2
        else:
            i += 1

    n = destroyed.first
    while n:
        r = n.value
        while 0 < r.start and r.stop < len(s):
            # Invariant: r has no adjacent range in destroyed.
            if reacting(s[r.start - 1], s[r.stop]):
                r = range(r.start - 1, r.stop + 1)
                if n.prev and n.prev.value.stop == r.start:
                    # Merge with previous
                    r = range(n.prev.value.start, r.stop)
                    destroyed.remove(n.prev)
                if n.next and n.next.value.start == r.stop:
                    # Merge with next
                    r = range(r.start, n.next.value.stop)
                    destroyed.remove(n.next)
                n.value = r
            else:
                break

        n = n.next

    return len(s) - sum(len(r) for r in destroyed)

def reduced(u):
    t = re.sub(u, '', s, flags=re.I)
    return reacted(t)

trials = [(u, reduced(u)) for u in units]

print(min(trials, key=lambda x: x[1]))
