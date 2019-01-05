#!/usr/bin/env python3

import fileinput
import re
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

byName = {}
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
    byName[name] = makeInst(f, proto)

prog = []
ipReg = None

for line in fileinput.input():
    m = re.match(r"#ip (\d+)", line)
    if m:
        assert ipReg is None
        assert len(prog) == 0
        ipReg = int(m.group(1))
        continue

    if line.startswith('exec'):
        name = 'exec'
        args = [line[5:]]
    else:
        name, *args = line.split()
        args = [int(x) for x in args]
    prog.append([name] + args)

regs = [0] * 6
regs[0] = 0
ip = 0
n = 0
seen = set()
while 0 <= ip < len(prog):
    inst = prog[ip]
    regs[ipReg] = ip
    if inst[0] == 'exec':
        exec(inst[1])
    else:
        f = byName[inst[0]]
        f(regs, inst[1:])
        n += 1
    if inst[:3] == ['eqrr', 1, 0]:
        if regs[1] in seen:
            print("Repeated:", hex(regs[1]), regs[1])
        seen.add(regs[1])
        print("@{}/{} {} {}".format(ip, n, inst, 
                                    " ".join("%x" % r for r in regs[:-1])))
    ip = regs[ipReg]
    ip += 1
print(n)
print(regs[0])

# vim: set shiftwidth=4 :