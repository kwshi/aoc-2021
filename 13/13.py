import collections as co
import itertools as it
import functools as ft
import sys
import numpy as np
import operator as op

def main():
    stuff = sys.stdin.read()
    a, b = stuff.strip().split('\n\n')
    pts = [tuple(map(int, s.split(','))) for s in a.strip().split()]
    folds = []
    for s in b.strip().split('\n'):
        c = s.split()[-1]
        y, z = c.split('=')
        folds.append((y, int(z)))

    grid = co.defaultdict(bool)
    for x, y in pts:
        grid[x, y] = True


    for var, pos in folds:
        if var == 'x':
            for x, y in [*grid]:
                if not grid[x, y]: continue
                if x > pos:
                    del grid[x, y]
                    grid[pos - (x-pos), y] = True
        if var == 'y':
            for x, y in [*grid]:
                if not grid[x, y]: continue
                if y > pos:
                    del grid[x, y]
                    grid[x, pos-(y-pos)] = True

    #print(sum(1 for _, v in grid.items() if v))

    xmin, xmax, ymin, ymax = 0, 0, 0, 0
    for x, y in grid:
        xmin = min(x, xmin)
        xmax = max(x, xmax)
        ymin = min(y, ymin)
        ymax = max(y, ymax)

    for y in range(ymin, ymax+1):
        for x in range(xmin, xmax+1):
            print('█' if grid[x, y] else ' ', end='')
        print()


main()

