#!/usr/bin/env python3

import fileinput
from collections import namedtuple

data = []
for line in fileinput.input():
    data.extend(int(w) for w in line.split())

Node = namedtuple('Node', 'children meta')

# Constructs a tree from a slice of data starting at index i
# Returns the tree and the number of elements used
def readTree(i):
    nChildren = data[i]
    nMeta = data[i + 1]
    n = 2
    i += 2
    children = []
    for _ in range(nChildren):
        c, m = readTree(i)
        children.append(c)
        i += m
        n += m
    meta = data[i:i + nMeta]
    n += nMeta
    return Node(children, meta), n

def metaSum(t):
    return sum(metaSum(c) for c in t.children) + sum(t.meta)

t, _ = readTree(0)
print(metaSum(t))
