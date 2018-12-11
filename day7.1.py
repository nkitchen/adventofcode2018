#!/usr/bin/env python3

import fileinput
import re
from collections import defaultdict
from sortedcontainers import SortedSet

nodes = set()
pendingBefore = defaultdict(int)
after = defaultdict(list)

for line in fileinput.input():
    m = re.search(r'Step (\S+) must be finished before step (\S+) can begin',
                  line)
    if not m:
        continue

    u = m.group(1)
    v = m.group(2)
    pendingBefore[v] += 1
    after[u].append(v)
    nodes.add(u)
    nodes.add(v)

nodesByPendingDeps = SortedSet()
for v in nodes:
    nodesByPendingDeps.add((pendingBefore[v], v))

steps = []
while len(nodesByPendingDeps):
    m, u = nodesByPendingDeps.pop(0)
    assert m == 0
    steps.append(u)

    for v in after[u]:
        n = pendingBefore[v]
        nodesByPendingDeps.remove((n, v))
        pendingBefore[v] = n - 1
        nodesByPendingDeps.add((n - 1, v))

print(''.join(steps))
