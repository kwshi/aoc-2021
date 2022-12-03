import collections as co
import functools as ft
import itertools as it
import pprint as pp
import dataclasses as dc

import kstricks.grid as grid
import heapq as hq
import re
import sys


def chunks(s):
    return s.strip().split("\n\n")


def lines(s):
    return s.strip().split("\n")


def bfs(graph, start, target):
    seen = {start}
    frontier = co.deque([start])
    while frontier:
        parent = frontier.popleft()
        for child in graph[parent]:
            if child == target:
                return
            if child in seen:
                continue
            seen.add(child)
            frontier.append(child)


def main():
    og = grid.Grid.from_stdin_char(conv=int)

    h, w = og.dims()
    g = grid.Grid.from_rows([[0] * (5 * w)] * (5 * h))
    for (i, j), val in og.items():
        for k, l in it.product(range(5), repeat=2):
            v = (val + l + k - 1) % 9 + 1
            g[k * h + i, l * w + j] = v

    seen = {}
    frontier = [(0, (0, 0))]
    while frontier:
        cost, parent = hq.heappop(frontier)
        if parent in seen:
            continue
        seen[parent] = cost
        h, w = g.dims()
        if parent == (h - 1, w - 1):
            print(cost)
            return
        for child in g.neighbors(parent):
            hq.heappush(frontier, (cost + g[child], child))


if __name__ == "__main__":
    main()
