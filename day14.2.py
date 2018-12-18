#!/usr/bin/env python3

import sys

def digits(n):
   d = []
   while True:
      d.append(n % 10)
      n //= 10
      if n == 0:
         break
   d.reverse()
   return d

target = digits(int(sys.argv[1]))
m = len(target)

recipes = [3, 7]
cur = [0, 1]

def run():
    while True:
        s = sum(recipes[i] for i in cur)

        d = digits(s)
        assert 1 <= len(d) <= 2

        recipes.extend(d)

        if len(d) == 2 and recipes[-m - 1:-1] == target:
            return len(recipes) - m - 1
        if recipes[-m:] == target:
            return len(recipes) - m

        for i, pos in enumerate(cur):
            cur[i] = (pos + recipes[pos] + 1) % len(recipes)

print(run())
