# pyright: strict
from __future__ import annotations
import sys
import itertools as it
import collections as co


class Image:
    alg: list[bool]
    img: dict[tuple[int, int], bool]
    default: bool

    def __init__(
        self,
        alg: list[bool],
        img: dict[tuple[int, int], bool],
        default: bool = False,
    ):
        self.alg = alg
        self.img = img
        self.default = default

    def __getitem__(self, pos: tuple[int, int]) -> bool:
        return self.img.get(pos, self.default)

    @staticmethod
    def neighbors(pos: tuple[int, int]):
        i, j = pos
        for di, dj in it.product([-1, 0, 1], repeat=2):
            yield i + di, j + dj

    def window(self, pos: tuple[int, int]):
        n = 0
        for p in Image.neighbors(pos):
            n = (n << 1) + self[p]
        return n

    def evolve(self) -> Image:
        new_img: dict[tuple[int, int], bool] = {}
        for p in self.img.keys():
            for q in Image.neighbors(p):
                if q not in new_img:
                    new_img[q] = self.alg[self.window(q)]

        new_default = self.alg[0b111111111] if self.default else self.alg[0]
        return Image(self.alg, new_img, new_default)

    def evolutions(self, n: int) -> Image:
        img = self
        for _ in range(n):
            img = img.evolve()
        return img

    def count(self) -> tuple[bool, int]:
        return (not self.default, co.Counter(self.img.values())[not self.default])


alg, chunk = sys.stdin.read().strip().split("\n\n")
img = Image(
    [c == "#" for c in "".join(alg.split())],
    {
        (i, j): c == "#"
        for i, line in enumerate(chunk.split("\n"))
        for j, c in enumerate(line.strip())
    },
)

print(img.evolutions(2).count())
print(img.evolutions(50).count())
