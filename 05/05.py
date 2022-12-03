import collections as co
import functools as ft
import itertools as it
import operator as op
import sys


def parse(s):
    a, b = s.split(" -> ")
    x1, y1 = map(int, a.split(","))
    x2, y2 = map(int, b.split(","))
    return (x1, y1), (x2, y2)


def main():
    s = sys.stdin.read().strip().split("\n")
    lines = [*map(parse, s)]

    grid = co.defaultdict(int)
    for (x1, y1), (x2, y2) in lines:
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                grid[x1, y] += 1
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                grid[x, y1] += 1
        else:
            dx = 1 if x2 > x1 else -1
            dy = 1 if y2 > y1 else -1
            print(x1, y1, x2, y2, dx, dy)
            for t in range(abs(y2 - y1) + 1):
                grid[x1 + t * dx, y1 + t * dy] += 1

    print(sum(1 for pos, ct in grid.items() if ct > 1))


if __name__ == "__main__":
    main()
