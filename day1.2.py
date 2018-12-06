#!/usr/bin/env python3

import fileinput

freqDeltas = []
for line in fileinput.input():
    freqDeltas.extend(map(int, line.split(',')))

def run():
    f = 0
    freqsSeen = set([f])
    while True:
        for d in freqDeltas:
            f += d
            if f in freqsSeen:
                return f
            freqsSeen.add(f)

print(run())
