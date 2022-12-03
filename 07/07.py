import collections as co
import functools as ft
import itertools as it
import operator as op
import sys

manhattan = lambda a, b: abs(a - b)
triangle = lambda a, b: abs(a - b) * (abs(a - b) + 1) // 2
find = lambda pos, dist: min(
    sum(dist(x, p) for p in pos) for x in range(min(pos), max(pos) + 1)
)


def main():
    pos = [*map(int, sys.stdin.read().strip().split(","))]
    print(find(pos, manhattan), find(pos, triangle))


main()
