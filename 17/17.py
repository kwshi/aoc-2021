import re
import math


def search(f):
    # find first t for which f(t) is True
    i, j = 0, 1
    while not f(j):
        j <<= 1
    while i < j:
        k = (i + j) >> 1
        if f(k):
            j = k
        else:
            i = k + 1

    assert f(i) and not f(i - 1)
    return i


"""
on step k (starting 0), Δx = vx-k, so
x(k) = vx*(k+1) - k*(k+1)/2 = (2*vx - k) * (k+1) / 2

but if k>vx, then Δx = 0 ≠ vx-k, so
x(k) = vx*(vx+1) / 2.
"""
x = lambda v, t: (2 * v - t) * (t + 1) // 2 if t <= v else v * (v + 1) // 2
y = lambda v, t: (2 * v - t) * (t + 1) // 2


def vels(x1, x2, y1, y2):

    vx_min = search(lambda vx: vx * (vx + 1) // 2 >= x1)
    vx_max = x2

    vy_min = y1
    vy_max = -y1

    for vx in range(vx_min, vx_max + 1):
        for vy in range(vy_min, vy_max + 1):
            tx1 = search(lambda t: x1 <= x(vx, t))
            tx2 = (
                math.inf
                if vx * (vx + 1) >> 1 <= x2
                else search(lambda t: x(vx, t) > x2) - 1
            )
            ty1 = search(lambda t: y(vy, t) <= y2)
            ty2 = search(lambda t: y(vy, t) < y1) - 1
            if ty1 <= ty2 and tx1 <= tx2 and tx2 >= ty1 and tx1 <= ty2:
                yield (vx, vy)


def main():
    grps = re.fullmatch(
        r"target area: x=([0-9]+)..([0-9]+), y=(-[0-9]+)..(-[0-9]+)", input()
    )
    assert grps
    x1, x2, y1, y2 = map(int, grps.groups())

    vs = [*vels(x1, x2, y1, y2)]

    vy = max(vy for _, vy in vs)
    print(vy * (vy + 1) >> 1)

    print(len(vs))


if __name__ == "__main__":
    main()


"""
maximum vx = x2 (otherwise overshoot)
minimum vx given by
  x1 ≤ vx (vx+1) / 2,
  2 x1 ≤ vx² + vx,
  vx² - vx ≥ 2 x1,
which implies, for vx ≥ 0,
  vx² ≥ 2 x1 + vx ≥ 2 x1.
Thus every vx ≥ minimum vx also satisfies
  vx ≥ √(2 x1).
"""

# vx_min = int(math.sqrt(2 * x1))
