#!/usr/bin/env python3

import collections
import fileinput
import re

data = collections.defaultdict(dict)

curGuard = None
sleepStart = None
for line in sorted(fileinput.input()):
    m = re.match(r'\[(?P<date>\d{4}-\d\d-\d\d) \d\d:(?P<min>\d\d)\] '
                 r'(?P<message>Guard #(?P<guardId>\d+) begins shift|falls asleep|wakes up)',
                 line)
    assert m
    minute = int(m.group('min'))
    g = m.group('guardId')
    if g:
        curGuard = int(g)
        continue

    if 'sleep' in m.group('message'):
        sleepStart = minute
    elif 'wake' in m.group('message'):
        data[curGuard].setdefault('sleepRanges', []).append(range(sleepStart, minute))
        sleepStart = None

def totalSleepTime(guard):
    return sum(map(len, data[guard]['sleepRanges']))

sleepiestGuard = max(data, key=totalSleepTime)

sleepCount = collections.defaultdict(int)
for r in data[sleepiestGuard]['sleepRanges']:
   for m in r:
      sleepCount[m] += 1
sleepiestMin, _ = max(sleepCount.items(), key=lambda kv: kv[1])
print(sleepiestGuard * sleepiestMin)
