#!/usr/bin/env python3

import copy
import pyllist
import fileinput

cartToTrack = {
    ord('>'): '-',
    ord('<'): '-',
    ord('^'): '|',
    ord('v'): '|',
}

carts = pyllist.dllist()
map = []
for y, line in enumerate(fileinput.input()):
    line = line.rstrip('\n')
    for x, c in enumerate(line):
        if c == '>':
            cart = dict(pos=(x, y), dir=(1, 0), nextTurn='L')
            carts.append(cart)
        elif c == '<':
            cart = dict(pos=(x, y), dir=(-1, 0), nextTurn='L')
            carts.append(cart)
        elif c == '^':
            cart = dict(pos=(x, y), dir=(0, -1), nextTurn='L')
            carts.append(cart)
        elif c == 'v':
            cart = dict(pos=(x, y), dir=(0, 1), nextTurn='L')
            carts.append(cart)
    line = line.translate(cartToTrack)
    map.append(line)

turned = {
    ((1, 0), '/'): (0, -1),
    ((1, 0), '\\'): (0, 1),
    ((1, 0), 'L'): (0, -1),
    ((1, 0), 'S'): (1, 0),
    ((1, 0), 'R'): (0, 1),
    ((-1, 0), '/'): (0, 1),
    ((-1, 0), '\\'): (0, -1),
    ((-1, 0), 'L'): (0, 1),
    ((-1, 0), 'S'): (-1, 0),
    ((-1, 0), 'R'): (0, -1),
    ((0, 1), '/'): (-1, 0),
    ((0, 1), '\\'): (1, 0),
    ((0, 1), 'L'): (1, 0),
    ((0, 1), 'S'): (0, 1),
    ((0, 1), 'R'): (-1, 0),
    ((0, -1), '/'): (1, 0),
    ((0, -1), '\\'): (-1, 0),
    ((0, -1), 'L'): (-1, 0),
    ((0, -1), 'S'): (0, -1),
    ((0, -1), 'R'): (1, 0),
}

turnSucc = {
    'L': 'S',
    'S': 'R',
    'R': 'L',
}

cartByPos = {}
for c in carts:
    cartByPos[c['pos']] = c

dirChar = {
    (1, 0): '>',
    (-1, 0): '<',
    (0, 1): 'v',
    (0, -1): '^',
}

def display():
    visMap = [list(line) for line in map]
    for c in carts:
        x, y = c['pos']
        visMap[y][x] = dirChar[c['dir']]
    for line in visMap:
        print(''.join(line))
    print("====")

def run():
    global carts

    while True:
        n = carts.first
        while n:
            c = n.value

            del cartByPos[c['pos']]

            x = c['pos'][0] + c['dir'][0]
            y = c['pos'][1] + c['dir'][1]
            if (x, y) in cartByPos:
                m = n.next
                carts.remove(n)
                n = m

                del cartByPos[(x, y)]

                m = carts.first
                while m:
                    if m.value['pos'] == (x, y):
                        if n and m.value == n.value:
                            n = n.next
                        k = m.next
                        carts.remove(m)
                        m = k
                    else:
                        m = m.next
            else:
                c['pos'] = (x, y)
                cartByPos[c['pos']] = c

                if map[y][x] in '/\\':
                    c['dir'] = turned[(c['dir'], map[y][x])]
                elif map[y][x] == '+':
                    c['dir'] = turned[(c['dir'], c['nextTurn'])]
                    c['nextTurn'] = turnSucc[c['nextTurn']]

                n = n.next

        #display()
        if len(carts) == 1:
            print(carts[0]['pos'])
            break

        carts = pyllist.dllist(sorted(carts, key=lambda c: c['pos']))

run()
