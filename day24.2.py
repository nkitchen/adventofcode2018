#!/usr/bin/env python3

import copy
import fileinput
import re

class Group():
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if type(v) == str and re.match(r"\d+$", v):
                kwargs[k] = int(v)

        w = kwargs.get("weaknesses") or ""
        kwargs["weaknesses"] = w.split(", ")

        im = kwargs.get("immunities") or ""
        kwargs["immunities"] = im.split(", ")

        for k, v in kwargs.items():
            if v:
                setattr(self, k, v)

    def effectivePower(self):
        return self.units * self.attackDamage

    def id(self):
        return (self.army, self.num)

    def damageDealtTo(self, otherGroup):
        if self.attackType in otherGroup.immunities:
            return 0

        ep = self.effectivePower()
        if self.attackType in otherGroup.weaknesses:
            return 2 * ep

        return ep

    def __repr__(self):
        return repr(self.__dict__)

army = None
armies = {}
k = None
for line in fileinput.input():
    m = re.search(r"^([\w ]+):$", line)
    if m:
        army = m.group(1)
        k = 1
        continue

    m = re.search(r"""(?x)(?P<units> \d+) [ ]units[ ]each
                      [ ]with[ ] (?P<hp>\d+) [ ]hit[ ]points
                      (?: [ ][(]
                        (?:
                          weak[ ]to[ ]
                          (?P<weaknesses> \w+ (?: ,[ ] \w+ )* )
                          (?: ;[ ] )?
                        |
                          immune[ ]to[ ]
                            (?P<immunities> \w+ (?: ,[ ] \w+ )* )
                            (?: ;[ ] )?
                        )*
                      [)] )?
                      [ ]with[ ]an[ ]attack[ ]that[ ]does[ ]
                      (?P<attackDamage> \d+ ) [ ]
                      (?P<attackType> \w+) [ ]damage
                      [ ]at[ ]initiative[ ] (?P<initiative> \d+ )
                      """,
                  line)
    if m:
        armies.setdefault(army, []).append(Group(**m.groupdict(),
                                                 army=army,
                                                 num=k))
        k += 1

assert len(armies) == 2

groups = {}
for a in armies.values():
    for g in a:
        groups[g.id()] = g

groups0 = groups

def fight(boost):
    groups = copy.deepcopy(groups0)

    for g in groups.values():
        if g.army == "Immune System":
            if not hasattr(g, "attackDamageOrig"):
                g.attackDamageOrig = g.attackDamage
            g.attackDamage = g.attackDamageOrig + boost

    while True:

        target = {}
        targetedBy = {}
        selectors = sorted(groups.values(), reverse=True,
                           key=lambda g: (g.effectivePower(), g.initiative))
        for g in selectors:
            defenders = [h for h in groups.values() if h.army != g.army
                                                    and h.id() not in targetedBy]
            if not defenders:
                continue

            defenders.sort(reverse=True,
                           key=lambda h: (g.damageDealtTo(h), h.effectivePower(), h.initiative))
            t = defenders[0]
            if g.damageDealtTo(t) > 0:
                target[g.id()] = t
                targetedBy[t.id()] = g.id()

        attackers = [groups[i] for i in target]
        attackers.sort(reverse=True, key=lambda g: g.initiative)

        totalKilled = 0

        for g in attackers:
            if g.units == 0:
                continue

            t = target[g.id()]
            d = g.damageDealtTo(t)
            killed = min(d // t.hp, t.units)
            t.units -= killed
            if t.units == 0:
                del groups[t.id()]
            totalKilled += killed

        if totalKilled == 0:
           return (None,-1)

        s = set(g.army for g in groups.values())
        if len(s) == 1:
            return (s.pop(), sum(g.units for g in groups.values()))

# 33 doesn't terminate
boostMin = 34 # 1
boostMax = 38 # 1000000

while boostMin < boostMax:
    boost = (boostMin + boostMax) // 2
    print((boostMin, boostMax, boost))
    army, n = fight(boost)
    if army == "Immune System":
        boostMax = boost
    else:
        boostMin = boost + 1
print(boostMin, n)
