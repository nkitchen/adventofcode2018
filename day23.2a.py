#!/usr/bin/env python3

import fileinput
import re
from collections import namedtuple

Nanobot = namedtuple('Nanobot', 'pos signalRadius')

nanobots = []

for line in fileinput.input():
    m = re.search(r"pos=<(-?\d+,-?\d+,-?\d+)>, r=(\d+)", line)
    if m:
        pos = [int(n) for n in m.group(1).split(",")]
        r = int(m.group(2))
        nanobots.append(Nanobot(pos, r))

import numpy as np

n = len(nanobots)
m = np.zeros((n, n))

for i in range(len(nanobots)):
    a = np.array(nanobots[i].pos)
    for j in range(i):
        b = np.array(nanobots[j].pos)
        d = abs(a - b).sum()
        if d <= nanobots[i].signalRadius + nanobots[j].signalRadius:
            m[i, j] = 1
            m[j, i] = 1

import pdb; pdb.set_trace()

"""
sum abs(p_i - a_i) <= r_a
sum abs(p_i - b_i) <= r_b
p_1 - a_1 
      b
  a  bbb
 aaabbbbb
aaa..bbbbb
 a..bbbbbbb
  abbbbbbb
    bbbbb
     bbb
      b
"""
