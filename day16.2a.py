#!/usr/bin/env python3

import fileinput
import numpy as np
from operator import *

def makeInst(f, proto):
    def inst(regs, args):
        inputs = [None, None]
        for i in range(2):
            if proto[i] == 'R':
                inputs[i] = regs[args[i]]
            elif proto[i] == 'V':
                inputs[i] = args[i]
        r = f(*inputs)
        regs[args[2]] = int(r)
    return inst

insts = []
for name, f, proto in [
    ('addr', add, 'RR'),
    ('addi', add, 'RV'),
    ('mulr', mul, 'RR'),
    ('muli', mul, 'RV'),
    ('banr', and_, 'RR'),
    ('bani', and_, 'RV'),
    ('borr', or_, 'RR'),
    ('bori', or_, 'RV'),
    ('setr', lambda a, b: a, 'RX'),
    ('seti', lambda a, b: a, 'VX'),
    ('gtir', gt, 'VR'),
    ('gtri', gt, 'RV'),
    ('gtrr', gt, 'RR'),
    ('eqir', eq, 'VR'),
    ('eqri', eq, 'RV'),
    ('eqrr', eq, 'RR'),
]:
    insts.append((name, makeInst(f, proto)))

lines = list(fileinput.input())

possibleCodes = {}
i = 0
while i < len(lines):
    line = lines[i]

    if line.startswith("Before:"):
        regsBefore = eval(line.split(maxsplit=1)[1])
        lineAfter = lines[i + 2]
        assert lineAfter.startswith("After:")
        regsAfter = eval(lineAfter.split(maxsplit=1)[1])

        code = [int(x) for x in lines[i + 1].split()]

        for name, inst in insts:
            regs = regsBefore[:]
            inst(regs, code[1:])
            if regs == regsAfter:
                possibleCodes.setdefault(name, set()).add(code[0])

        i += 3
    else:
        i += 1

m = np.zeros((len(possibleCodes), 16), dtype=int)
for i, name in enumerate(sorted(possibleCodes)):
    for j in possibleCodes[name]:
        m[i][j] = 1
print(m)
