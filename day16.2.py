#!/usr/bin/env python3

import fileinput
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

byOpcode = {}
for name, opcode, f, proto in [
    ('addr', 4, add, 'RR'),
    ('addi', 2, add, 'RV'),
    ('mulr', 12, mul, 'RR'),
    ('muli', 3, mul, 'RV'),
    ('banr', 15, and_, 'RR'),
    ('bani', 5, and_, 'RV'),
    ('borr', 1, or_, 'RR'),
    ('bori', 0, or_, 'RV'),
    ('setr', 7, lambda a, b: a, 'RX'),
    ('seti', 9, lambda a, b: a, 'VX'),
    ('gtir', 14, gt, 'VR'),
    ('gtri', 6, gt, 'RV'),
    ('gtrr', 8, gt, 'RR'),
    ('eqir', 10, eq, 'VR'),
    ('eqri', 13, eq, 'RV'),
    ('eqrr', 11, eq, 'RR'),
]:
    byOpcode[opcode] = makeInst(f, proto)

regs = [0] * 4
for line in fileinput.input():
    code = [int(x) for x in line.split()]
    inst = byOpcode[code[0]]
    inst(regs, code[1:])
print(regs[0])
