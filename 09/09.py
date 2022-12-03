import heapq
import math
import sys

import kstricks.grid as grid


def main():
    g = grid.Grid.from_rows(map(int, line.strip()) for line in sys.stdin)

    low = {p: v for p, v in g.items() if all(g[q] > v for q in g.neighbors(p))}
    print(sum(low.values()) + len(low))

    basins = {p: [p] for p in low}
    seen = {p: p for p in low}
    frontier = [*low.keys()]
    while frontier:
        p = frontier.pop()
        for q in g.neighbors(p):
            if q in seen or g[q] == 9:
                continue
            frontier.append(q)
            seen[q] = seen[p]
            basins[seen[p]].append(q)
    print(math.prod(heapq.nlargest(3, map(len, basins.values()))))


if __name__ == "__main__":
    main()
