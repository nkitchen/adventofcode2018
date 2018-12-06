#!/usr/bin/env python3

import fileinput

s = 0
for line in fileinput.input():
    s += sum(map(int, line.split(',')))
print(s)
