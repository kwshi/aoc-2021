import collections as co
import functools as ft
import itertools as it
import operator as op
import sys

digits = [
    (0, 1, 2, 4, 5, 6),
    (2, 5),
    (0, 2, 3, 4, 6),
    (0, 2, 3, 5, 6),
    (1, 2, 3, 5),
    (0, 1, 3, 5, 6),
    (0, 1, 3, 4, 5, 6),
    (0, 2, 5),
    (0, 1, 2, 3, 4, 5, 6),
    (0, 1, 2, 3, 5, 6),
]

decoders = {}
for perm in it.permutations("abcdefg"):
    decoder = {"".join(sorted(perm[i] for i in pat)): n for n, pat in enumerate(digits)}
    decoders[tuple(sorted(decoder.keys()))] = decoder


def solve(pats, sig):
    decoder = decoders[tuple(sorted("".join(sorted(pat)) for pat in pats))]
    return [decoder["".join(sorted(s))] for s in sig]


def main():
    cases = []
    for line in sys.stdin:
        pats, sig = line.strip().split(" | ")
        cases.append(solve(pats.split(), sig.split()))

    p1 = sum(1 for a in cases for b in a if b in {1, 4, 7, 8})
    p2 = sum(int("".join(map(str, dig))) for dig in cases)

    print(p1, p2)


main()
