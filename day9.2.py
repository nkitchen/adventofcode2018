#!/usr/bin/env python3

import fileinput
import itertools
import pyllist
import re
from collections import defaultdict

def main():
    for line in fileinput.input():
        m = re.search(r'(\d+) players; last marble is worth (\d+) points', line)
        if not m:
            continue

        nPlayers = int(m.group(1))
        lastMarble = int(m.group(2))
        s = highScore(nPlayers, lastMarble * 100)
        print("{nPlayers}; {lastMarble}: {s}".format(**locals()))

def highScore(nPlayers, lastMarble):
    circle = pyllist.dllist()
    cur = circle.append(0)

    def _fwd(i):
        i = i.next
        if not i:
            i = circle.first
        return i

    def _rev(i):
        i = i.prev
        if not i:
            i = circle.last
        return i

    score = defaultdict(int)
    players = range(1, nPlayers + 1)
    marbles = range(1, lastMarble + 1)
    for player, marble in zip(itertools.cycle(players), marbles):
        if marble % 23:
            cur = _fwd(cur)
            cur = circle.insert(marble, after=cur)
        else:
            score[player] += marble
            for _ in range(7):
                cur = _rev(cur)
            score[player] += cur.value
            n = cur
            cur = _fwd(cur)
            circle.remove(n)
    return max(score.values())


if __name__ == '__main__':
    main()
