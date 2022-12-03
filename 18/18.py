import sys
import collections as co
import dataclasses as dc
import itertools as it
import functools as ft
import re
import math
import operator as op

total = []
for line in sys.stdin:
    stuff = eval(line.strip())
    total.append(stuff)

everything = ft.reduce(lambda a, b: [a, b], total)


def magnitude(something):
    if isinstance(something, int):
        return something
    a, b = something
    return 3 * magnitude(a) + 2 * magnitude(b)


def leaves(something):
    if isinstance(something, int):
        yield something
        return
    a, b = something
    yield from leaves(a)
    yield from leaves(b)


def split(something):
    pass


def leftmost(something, x: int):
    if isinstance(something, int):
        return
    a, b = something
    if isinstance(a, int):
        something[0] += x
    else:
        leftmost(a, x)


def rightmost(something, x):
    a, b = something
    if isinstance(b, int):
        something[1] += x
    else:
        rightmost(b, x)


def explode(something, level=0):
    if isinstance(something, int):
        return None, None
    if level >= 4 and isinstance(something[0], int) and isinstance(something[1], int):
        return something

    # check if any children are exploded
    a, b = something
    al, ar = explode(a, level + 1)
    if ar is not None:
        if al is not None:
            something[0] = 0
        if isinstance(b, int):
            something[1] += ar
        else:
            leftmost(b, ar)
        return al, None

    bl, br = explode(b, level + 1)
    if bl is not None:
        # print("aaa", bl, br)
        if br is not None:
            something[1] = 0
        if isinstance(a, int):
            something[0] += bl
        else:
            rightmost(a, bl)
        return None, br

    return None, None


def split(thing):
    if isinstance(thing, int):
        if thing >= 10:
            a = thing // 2
            b = thing - a
            return [a, b]
        return

    a, b = thing
    sa = split(a)
    if sa is not None:
        thing[0] = sa
        return
    sb = split(b)
    if sb is not None:
        thing[1] = sb
        return


def reduce(some):
    for _ in range(200):
        explode(some)
        split(some)


# print(magnitude(everything))
# thing = [[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]]
# thing = [[[[[9, 8], 1], 2], 3], 4]
# thing = [[[[0, 7], 4], [15, [0, 13]]], [1, 1]]
# reduce(thing)
reduce(everything)
print(magnitude(everything))
