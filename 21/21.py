# pyright: strict
from __future__ import annotations
import itertools as it
import collections as co
import dataclasses as dc
import re
import typing as t

T = t.TypeVar("T")

# useful kstricks utility for simulating multi-worlds: dictionary mapping state to counts, evolve accordingly


def deterministic_dice() -> t.Iterable[int]:
    return it.cycle(range(1, 101))


def deterministic_pairs() -> t.Iterable[tuple[int, int]]:
    dice = deterministic_dice()
    triples = map(sum, zip(dice, dice, dice))
    return zip(triples, triples)


@dc.dataclass(frozen=True)
class State:
    p1: int
    p2: int
    s1: int = 0
    s2: int = 0
    r: int = 0  # number of rolls

    def m1(self, size: int) -> State:
        p = (self.p1 + size - 1) % 10 + 1
        return State(p, self.p2, self.s1 + p, self.s2, self.r + 3)

    def m2(self, size: int) -> State:
        p = (self.p2 + size - 1) % 10 + 1
        return State(self.p1, p, self.s1, self.s2 + p, self.r + 3)

    @staticmethod
    def parse() -> State:
        pat = re.compile(r"Player [12] starting position: ([0-9]+)")
        i1 = pat.fullmatch(input())
        i2 = pat.fullmatch(input())
        assert i1 is not None
        assert i2 is not None
        return State(int(i1[1]), int(i2[1]))

    def deterministic(self) -> int:
        state: State = self
        for d1, d2 in deterministic_pairs():
            state = state.m1(d1)
            if state.s1 >= 1000:
                return state.r * state.s2
            state = state.m2(d2)
            if state.s2 >= 1000:
                return state.r * state.s1
        raise ValueError("dice should never terminate")

    def dirac(self) -> int:
        step = co.Counter(map(sum, it.product([1, 2, 3], repeat=3)))
        world = {self: 1}
        w1 = w2 = 0
        while world:
            new = co.defaultdict(int)
            for state, ct in world.items():
                for size, n in step.items():
                    state1 = state.m1(size)
                    times = ct * n
                    if state1.s1 >= 21:
                        w1 += times
                    else:
                        new[state1] += times


if __name__ == "__main__":
    start = State.parse()
    print(start.deterministic())
