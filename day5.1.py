#!/usr/bin/env python3

import fileinput

s = next(fileinput.input()).strip()

def reacting(c, d):
    return c.lower() == d.lower() and c.islower() != d.islower()

destroyed = []

i = 0
while i < len(s) - 1:
    if reacting(s[i], s[i + 1]):
        destroyed.append(range(i, i + 2))
        i += 2
    else:
        i += 1

# Postcondition: a is a list of non-adjacent ranges.
def mergeRanges(a):
    i = 0
    while i < len(a) - 1:
        if a[i].stop == a[i + 1].start:
            a[i] = range(a[i].start, a[i + 1].stop)
            a.pop(i + 1)
        else:
            i += 1

# Precondition: destroyed is a list of non-adjacent ranges
def growGaps():
    def _grow(j):
        grew = False
        r = destroyed[j]
        while True:
            if r.start == 0:
                return grew
            if r.stop == len(s):
                return grew
            if j > 0 and r.start == destroyed[j - 1].stop:
                return grew
            if j < len(destroyed) - 1 and r.stop == destroyed[j + 1].start:
                return grew
            if reacting(s[r.start - 1], s[r.stop]):
                r = range(r.start - 1, r.stop + 1)
                destroyed[j] = r
                grew = True
            else:
                return grew

    return any(_grow(i) for i in range(len(destroyed)))

mergeRanges(destroyed)
while growGaps():
    mergeRanges(destroyed)

print(len(s) - sum(len(r) for r in destroyed))
    
