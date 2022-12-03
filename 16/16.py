# pyright: strict
from __future__ import annotations
import math
import typing
import dataclasses as dc


@dc.dataclass
class Packet:
    ver: int
    data: Operator | Literal

    def versions(self) -> typing.Generator[int, None, None]:
        yield self.ver
        if isinstance(self.data, Operator):
            for subtree in self.data.args:
                yield from subtree.versions()

    def evaluate(self) -> int:
        return self.data.evaluate()


@dc.dataclass
class Operator:
    tid: int
    args: list[Packet]

    def evaluate(self) -> int:
        vals = [arg.evaluate() for arg in self.args]
        match self.tid:
            case 0:
                return sum(vals)
            case 1:
                return math.prod(vals)
            case 2:
                return min(vals)
            case 3:
                return max(vals)
            case 5:
                return int(vals[0] > vals[1])
            case 6:
                return int(vals[0] < vals[1])
            case 7:
                return int(vals[0] == vals[1])
            case _:
                raise ValueError(f"invalid typeid {self.tid}, args {self.args}")


@dc.dataclass
class Literal:
    val: int

    def evaluate(self) -> int:
        return self.val


def parse(data: str):
    bits = "".join(f"{int(c, 16):04b}" for c in data)
    packet, _ = parse_packet(bits, 0)
    return packet


def parse_value(bits: str, pos: int):
    chunks: list[str] = []
    while True:
        first, chunk = bits[pos], bits[pos + 1 : pos + 5]
        pos += 5

        chunks.append(chunk)

        if first == "0":
            break

    val = int("".join(chunks), 2)
    return val, pos


def parse_children(bits: str, pos: int):
    lt = bits[pos]
    pos += 1
    children: list[Packet] = []
    if lt == "0":
        size = int(bits[pos : pos + 15], 2)
        pos += 15
        end = pos + size
        while pos < end:
            packet, pos = parse_packet(bits, pos)
            children.append(packet)
        assert pos == end, (pos, end)
    else:
        size = int(bits[pos : pos + 11], 2)
        pos += 11
        for _ in range(size):
            packet, pos = parse_packet(bits, pos)
            children.append(packet)
    return children, pos


def parse_data(bits: str, pos: int, tid: int):
    if tid == 4:
        val, pos = parse_value(bits, pos)
        return Literal(val), pos
    else:
        children, pos = parse_children(bits, pos)
        return Operator(tid, children), pos


def parse_packet(bits: str, pos: int):
    ver = int(bits[pos : pos + 3], 2)
    tid = int(bits[pos + 3 : pos + 6], 2)
    data, pos = parse_data(bits, pos + 6, tid)
    return Packet(ver, data), pos


def main():
    tree = parse(input())

    print(sum(tree.versions()))
    print(tree.evaluate())


if __name__ == "__main__":
    main()
