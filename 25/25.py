import sys
import pprint as pp
import itertools as it

grid = [line.strip() for line in sys.stdin]


def evolve(grid: list[str]) -> list[str]:
    h, w = len(grid), len(grid[0])

    east = [["." for _ in range(w)] for _ in range(h)]
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if c == ">":
                if grid[i][(j + 1) % w] == ".":
                    east[i][(j + 1) % w] = ">"
                else:
                    east[i][j] = ">"
            elif c == "v":
                east[i][j] = "v"

    south = [["." for _ in range(w)] for _ in range(h)]
    for i, row in enumerate(east):
        for j, c in enumerate(row):
            if c == "v":
                if east[(i + 1) % h][j] == ".":
                    south[(i + 1) % h][j] = "v"
                else:
                    south[i][j] = "v"
            elif c == ">":
                south[i][j] = ">"

    return ["".join(line) for line in south]


evolved = grid
for i in it.count():
    new = evolve(evolved)
    if new == evolved:
        print(i + 1)
        break
    evolved = new
