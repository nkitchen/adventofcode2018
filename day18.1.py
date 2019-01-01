#!/usr/bin/env python3

import copy
import fileinput

acre = []

for line in fileinput.input():
    acre.append(list(line.rstrip()))
m = len(acre)
n = len(acre[0])

for i in range(1000):
    acreNew = copy.deepcopy(acre)
    for i in range(m):
        a = max(0, i - 1)
        b = min(m - 1, i + 1)
        for j in range(n):
            c = max(0, j - 1)
            d = min(n - 1, j + 1)

            nTree = 0
            nLumber = 0
            for u in range(a, b + 1):
                for v in range(c, d + 1):
                    if u == i and v == j:
                        continue
                    if acre[u][v] == '|':
                        nTree += 1
                    if acre[u][v] == '#':
                        nLumber += 1

            if acre[i][j] == '.':
                if nTree >= 3:
                    acreNew[i][j] = '|'
            elif acre[i][j] == '|':
                if nLumber >= 3:
                    acreNew[i][j] = '#'
            elif acre[i][j] == '#':
                if nLumber >= 1 and nTree >= 1:
                    pass
                else:
                    acreNew[i][j] = '.'
    acre = acreNew

nTree = 0
nLumber = 0
for row in acre:
    for v in row:
        if v == '|':
            nTree += 1
        elif v == '#':
            nLumber += 1
print(nTree * nLumber)
