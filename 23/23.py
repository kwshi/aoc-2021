from __future__ import annotations

import dataclasses as dc
import itertools as it
import typing as t
import heapq as hq
import pprint as pp


Amphipod = t.Literal["A"] | t.Literal["B"] | t.Literal["C"] | t.Literal["D"]
Stack = tuple[Amphipod, Amphipod]
PStack = tuple[Amphipod, ...]

costs: dict[Amphipod, int] = {"A": 1, "B": 10, "C": 100, "D": 1000}


@dc.dataclass(frozen=True)
class Arrangement:
    pos: tuple[Stack, Stack, Stack, Stack]

    @staticmethod
    def parse_line() -> list[Amphipod]:
        return [t.cast(Amphipod, c) for c in input() if c in costs.keys()]

    @staticmethod
    def parse():
        input()
        input()
        pos = t.cast(
            tuple[Stack, Stack, Stack, Stack],
            tuple(zip(Arrangement.parse_line(), Arrangement.parse_line())),
        )
        return Arrangement(pos)

    @staticmethod
    def terminals() -> t.Iterable[Arrangement]:
        for w, x, y, z in it.permutations("ABCD"):
            yield Arrangement(((w, w), (x, x), (y, y), (z, z)))


@dc.dataclass(frozen=True, order=True)
class Situation:
    pos: tuple[PStack, ...]
    hallway: tuple[Amphipod | t.Literal[""], ...] = tuple("" for _ in range(11))

    def neighbors(self) -> t.Iterable[tuple[int, Situation]]:
        # move out of room for the first time
        for i, p in enumerate(self.pos):
            if not p:  # nothing to move
                continue

            rest, mover = p[:-1], p[-1]

            # move right
            x = (1 + i) * 2
            for j in range(x + 1, 11):
                if j in [2, 4, 6, 8]:  # room slots
                    continue
                if self.hallway[j]:  # blocked
                    break
                # if len(p) == 2, then one step to enter hallway;
                # if 1, then two steps.
                cost = costs[mover] * ((3 - len(p)) + (j - x))
                new_pos = [*self.pos]
                new_pos[i] = rest
                new_hallway = list(self.hallway)  # TODO pyright error when [*]
                new_hallway[j] = mover
                assert cost > 0
                yield cost, Situation(tuple(new_pos), tuple(new_hallway))

            # move left
            for j in range(x - 1, -1, -1):
                if j in [2, 4, 6, 8]:  # room slots
                    continue
                if self.hallway[j]:  # blocked
                    break
                cost = costs[mover] * ((3 - len(p)) + (x - j))
                new_pos = [*self.pos]
                new_pos[i] = rest
                new_hallway = list(self.hallway)  # TODO pyright error when [*]
                new_hallway[j] = mover
                assert cost > 0
                yield cost, Situation(tuple(new_pos), tuple(new_hallway))

        # move into final room
        for i, a in enumerate(self.hallway):
            if not a:
                continue

            # target rooms on right
            for j in range(i + 1, 9):
                if j not in [2, 4, 6, 8]:
                    continue
                if self.hallway[j]:
                    break
                r = j // 2 - 1
                room = self.pos[r]
                if len(room) == 2:
                    continue
                # if room is 1, then takes 1 cost; if empty, then takes 2 steps
                cost = costs[a] * ((j - i) + (2 - len(room)))
                new_hallway = list(self.hallway)
                new_hallway[i] = ""
                new_pos = list(self.pos)
                new_pos[r] = room + (a,)
                assert cost > 0
                yield cost, Situation(tuple(new_pos), tuple(new_hallway))

            # target rooms on left
            for j in range(i - 1, 1, -1):
                if j not in [2, 4, 6, 8]:
                    continue
                if self.hallway[j]:
                    break
                r = j // 2 - 1
                room = self.pos[r]
                if len(room) == 2:
                    continue
                if room and room[0] != a:  # can't finalize
                    continue
                # if room is 1, then takes 1 cost; if empty, then takes 2 steps
                cost = costs[a] * ((i - j) + (2 - len(room)))
                new_hallway = list(self.hallway)
                new_hallway[i] = ""
                new_pos = list(self.pos)
                new_pos[r] = room + (a,)
                assert len(room) <= 2
                assert cost > 0
                yield cost, Situation(tuple(new_pos), tuple(new_hallway))

        # TODO account for refusal to re-leave the room

    def done(self) -> bool:
        return all(len(p) == 2 and p[0] == p[1] for p in self.pos)

    def pprint(self):
        print("#" * 13)
        print(f"#{''.join(c or '.' for c in self.hallway)}#")
        print(f"###{'#'.join(p[1] if len(p) == 2 else '.' for p in self.pos)}###")
        print(f"  #{'#'.join(p[0] if p else '.' for p in self.pos)}#")
        print("  #########")

    @staticmethod
    def from_arrangement(a: Arrangement) -> Situation:
        return Situation(a.pos)


def distance(a1: Arrangement) -> int:
    frontier: list[tuple[int, Situation]] = [(0, Situation.from_arrangement(a1))]
    done = {}
    while frontier:
        dist, parent = hq.heappop(frontier)
        print(dist, "parent")
        parent.pprint()
        print()
        done[parent] = dist

        if parent.done():
            return dist

        for cost, new in parent.neighbors():
            if new in done:
                continue
            # print("child", dist + cost)
            # new.pprint()
            # print()
            hq.heappush(frontier, (dist + cost, new))

    print(done)
    return -1


arr = Arrangement.parse()
print(distance(arr))
