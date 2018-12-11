#!/usr/bin/env python3

import fileinput
import re
from collections import defaultdict
from collections import namedtuple
from sortedcontainers import SortedSet

Availability = namedtuple('Availability', 'time workerId')
Work = namedtuple('Work', 'time id')

def duration(w):
    return ord(w) - ord('A') + 1 + 60

nWorkers = 5

tasks = set()
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
    tasks.add(u)
    tasks.add(v)

workerAvailability = SortedSet()
for i in range(nWorkers):
    workerAvailability.add(Availability(0, i))

workQueue = SortedSet()
for w in tasks:
    if pendingBefore[w] == 0:
        workQueue.add(Work(0, w))

Step = namedtuple('Step', 'timeDone id')
completions = SortedSet()

while len(workQueue):
    tw, w = workQueue.pop(0)
    av = workerAvailability.pop(0)
    t = max(tw, av.time)

    d = duration(w)
    completions.add(Step(t + d, w))
    workerAvailability.add(Availability(t + d, av.workerId))

    for x in after[w]:
        n = pendingBefore[x]
        if n == 1:
            workQueue.add(Work(t + d, x))
        pendingBefore[x] = n - 1

print(completions[-1].timeDone)
