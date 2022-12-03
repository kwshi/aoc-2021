from __future__ import annotations
import sys
import re
import itertools as it
import dataclasses as dc

pat_int = r"(-?[0-9]+)"
re_instruction = re.compile(
    rf"(on|off) x={pat_int}\.\.{pat_int},y={pat_int}\.\.{pat_int},z={pat_int}\.\.{pat_int}"
)


def parse_instruction(s: str) -> tuple[bool, Cuboid]:
    result = re_instruction.fullmatch(s)
    assert result is not None
    state, x1, x2, y1, y2, z1, z2 = result.groups()
    return state == "on", Cuboid(
        int(x1), int(x2) + 1, int(y1), int(y2) + 1, int(z1), int(z2) + 1
    )


@dc.dataclass(frozen=True)
class Cuboid:
    x1: int
    x2: int
    y1: int
    y2: int
    z1: int
    z2: int

    def intersects(self, other: Cuboid):
        return (
            self.x1 < other.x2
            and other.x1 < self.x2
            and self.y1 < other.y2
            and other.y1 < self.y2
            and self.z1 < other.z2
            and other.z1 < self.z2
        )

    def within(self, other: Cuboid):
        return (
            other.x1 <= self.x1
            and self.x2 <= other.x2
            and other.y1 <= self.y1
            and self.y2 <= other.y2
            and other.z1 <= self.z1
            and self.z2 <= other.z2
        )

    def volume(self):
        return (self.x2 - self.x1) * (self.y2 - self.y1) * (self.z2 - self.z1)

    def intersection(self, other: Cuboid):
        x1, x2 = max(self.x1, other.x1), min(self.x2, other.x2)
        y1, y2 = max(self.y1, other.y1), min(self.y2, other.y2)
        z1, z2 = max(self.z1, other.z1), min(self.z2, other.z2)
        if x1 >= x2 or y1 >= y2 or z1 >= z2:
            return None
        return Cuboid(x1, x2, y1, y2, z1, z2)

    def split(self, other: Cuboid):
        parts = []
        for (x1, x2), (y1, y2), (z1, z2) in it.product(
            it.pairwise(sorted([self.x1, other.x1, other.x2, self.x2])),
            it.pairwise(sorted([self.y1, other.y1, other.y2, self.y2])),
            it.pairwise(sorted([self.z1, other.z1, other.z2, self.z2])),
        ):
            cube = Cuboid(x1, x2, y1, y2, z1, z2)
            if x1 == x2 or y1 == y2 or z1 == z2:
                continue
            if cube.within(self) and not cube.within(other):
                parts.append(cube)
        return parts


instructions = [parse_instruction(line.strip()) for line in sys.stdin]


def p2():
    # disjoint partitioning into cubes
    cubes: list[Cuboid] = []
    for (state, cube) in instructions:
        new: list[Cuboid] = []

        for prev in cubes:
            if not cube.intersects(prev):
                new.append(prev)
                continue

            for part in prev.split(cube):
                new.append(part)

        if state:
            new.append(cube)

        cubes = new

    print(sum(cube.volume() for cube in cubes))


p2()
