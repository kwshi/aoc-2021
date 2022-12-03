from __future__ import annotations
import sys
import collections as co
import typing as t
import itertools as it
import dataclasses as dc
import pprint as pp
import functools as ft
import math


@dc.dataclass
class Pt:
    x: int
    y: int
    z: int

    def orientations(self):
        rots = [
            self,
            Pt(self.x, -self.z, self.y),
            Pt(self.x, -self.y, -self.z),
            Pt(self.x, self.z, -self.y),
            Pt(-self.y, self.x, self.z),
            Pt(self.z, self.x, self.y),
            Pt(self.y, self.x, -self.z),
            Pt(-self.z, self.x, -self.y),
            Pt(self.y, self.z, self.x),
            Pt(-self.z, self.y, self.x),
            Pt(-self.y, -self.z, self.x),
            Pt(self.z, -self.y, self.x),
            Pt(-self.x, -self.y, self.z),
            Pt(-self.x, self.z, self.y),
            Pt(-self.x, self.y, -self.z),
            Pt(-self.x, -self.z, -self.y),
            Pt(self.y, -self.x, self.z),
            Pt(-self.z, -self.x, self.y),
            Pt(-self.y, -self.x, -self.z),
            Pt(self.z, -self.x, -self.y),
            Pt(-self.y, self.z, -self.x),
            Pt(self.z, self.y, -self.x),
            Pt(self.y, -self.z, -self.x),
            Pt(-self.z, -self.y, -self.x),
        ]
        return rots

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __add__(self, other: Pt):
        return Pt(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Pt):
        return Pt(self.x - other.x, self.y - other.y, self.z - other.z)

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __lt__(self, other: Pt):
        return tuple(self) < tuple(other)

    def __neg__(self):
        return Pt(-self.x, -self.y, -self.z)

    def __str__(self):
        return f"({self.x},{self.y},{self.z})"

    def __repr__(self):
        return f"({self.x},{self.y},{self.z})"


def parse_pt(s: str) -> Pt:
    a, b, c = map(int, s.split(","))
    return Pt(a, b, c)


def parse():
    chunks = sys.stdin.read().strip().split("\n\n")
    scans = {
        i: {*map(parse_pt, chunk.split("\n")[1:])} for i, chunk in enumerate(chunks)
    }
    return scans


# assume 0 is objective
scans = parse()


# @ft.lru_cache(None)
# def align(a: int, ):

start = {*scans[0]}
unseen = {*scans.keys()} - {0}
scanners = {0: Pt(0, 0, 0)}
while unseen:
    added = set()
    for candidate in unseen:
        partial = scans[candidate]

        found = False

        # iterate over each point, try all orientations relative to point, etc.
        for src, tgt in it.product(start, partial):
            transforms = [set() for _ in range(24)]
            for pt in partial:
                for i, orient in enumerate((pt - tgt).orientations()):
                    transforms[i].add(orient + src)

            for i, transform in enumerate(transforms):
                if len(transform & start) >= 12:
                    start |= transform
                    found = True

                    if found:
                        scanners[candidate] = (Pt(0, 0, 0) - tgt).orientations()[
                            i
                        ] + src

                    break

        if found:
            added.add(candidate)

    unseen -= added

# print(len(start))
def dist(a: Pt, b: Pt):
    c = a - b
    return abs(c.x) + abs(c.y) + abs(c.z)


print(max(dist(a, b) for a, b in it.combinations(scanners.values(), 2)))
