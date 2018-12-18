#!/usr/bin/env python3

import sys

n = int(sys.argv[1])

recipes = [3, 7]
cur = [0, 1]

while len(recipes) < n + 10:
    s = sum(recipes[i] for i in cur)
    digits = [s % 10]
    s //= 10
    while s > 0:
        digits.append(s % 10)
        s //= 10

    recipes.extend(reversed(digits))

    for i, pos in enumerate(cur):
        cur[i] = (pos + recipes[pos] + 1) % len(recipes)

print(''.join(map(str, recipes[n:n+10])))
