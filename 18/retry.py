# pyright: strict

from __future__ import annotations
import dataclasses as dc
import typing as t
import sys
import itertools as it


@dc.dataclass
class Pair:
    l: Node
    r: Node

    def __str__(self):
        return f"[{self.l},{self.r}]"

    def clone(self) -> Pair:
        return Pair(self.l.clone(), self.r.clone())


@dc.dataclass
class Node:
    val: Pair | int

    def __add__(self, other: Node):
        return Node(Pair(self, other)).clone()

    def __str__(self):
        return str(self.val)

    def combine_left(self, x: int):
        if isinstance(self.val, int):
            self.val += x
        else:
            self.val.l.combine_left(x)

    def combine_right(self, x: int):
        if isinstance(self.val, int):
            self.val += x
        else:
            self.val.r.combine_right(x)

    def clone(self) -> Node:
        if isinstance(self.val, int):
            return Node(self.val)
        return Node(self.val.clone())

    def _explode(self, depth: int = 0) -> tuple[bool, int | None, int | None]:
        if isinstance(self.val, int):
            return False, None, None

        if (
            depth >= 4
            and isinstance(self.val.l.val, int)
            and isinstance(self.val.r.val, int)
        ):
            r = True, self.val.l.val, self.val.r.val
            self.val = 0
            return r

        if isinstance(self.val.l.val, Pair):
            exploded, l, r = self.val.l._explode(depth + 1)
            if r is not None:
                self.val.r.combine_left(r)
            if exploded:
                return True, l, None

        if isinstance(self.val.r.val, Pair):
            exploded, l, r = self.val.r._explode(depth + 1)
            if l is not None:
                self.val.l.combine_right(l)
            if exploded:
                return True, None, r

        return False, None, None

    def explode(self) -> bool:
        return self._explode()[0]

    def split(self) -> bool:
        if isinstance(self.val, int):
            if self.val >= 10:
                a = self.val // 2
                self.val = Pair(Node(a), Node(self.val - a))
                return True
            return False

        return self.val.l.split() or self.val.r.split()

    def mag(self) -> int:
        if isinstance(self.val, int):
            return self.val

        return 3 * self.val.l.mag() + 2 * self.val.r.mag()

    def reduce(self):
        while True:
            if self.explode():
                continue
            elif self.split():
                continue
            else:
                break


def to_node(l: t.Any) -> Node:
    if isinstance(l, int):
        return Node(l)
    a, b = l
    return Node(Pair(to_node(a), to_node(b)))


def parse(x: str) -> Node:
    return to_node(eval(x))


nums: list[Node] = []
for line in sys.stdin:
    nums.append(parse(line.strip()))

stuff: list[int] = []
for m, n in it.combinations(nums, 2):
    a = m + n
    a.reduce()
    stuff.append(a.mag())

    b = n + m
    b.reduce()
    stuff.append(b.mag())

print(max(stuff))
