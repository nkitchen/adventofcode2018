#!/usr/bin/env python3

import collections
import fileinput

ids = [line.strip() for line in fileinput.input()]

for i, a in enumerate(ids[:-1]):
    for b in ids[i + 1:]:
        d = set(enumerate(a)) ^ set(enumerate(b))
        if len(d) != 2:
            continue

        (i, x), (j, y) = list(d)
        assert i == j
        print(a[:i] + a[i + 1:])
