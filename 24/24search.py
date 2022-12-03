# pyright: strict
from __future__ import annotations
import dataclasses as dc
import operator as op
import typing as t
import sys

ops: dict[str, t.Callable[[int, int], int]] = {
    "add": op.add,
    "mul": op.mul,
    "mod": op.mod,
    "div": op.floordiv,
    "eql": lambda a, b: int(a == b),
}


@dc.dataclass(frozen=True, slots=True)
class State:
    w: int
    x: int
    y: int
    z: int

    def __getitem__(self, k: str) -> int:
        match k:
            case "w":
                return self.w
            case "x":
                return self.x
            case "y":
                return self.y
            case "z":
                return self.z
            case _:
                return int(k)

    def set(self, k: str, v: int) -> State:
        match k:
            case "w":
                return State(v, self.x, self.y, self.z)
            case "x":
                return State(self.w, v, self.y, self.z)
            case "y":
                return State(self.w, self.x, v, self.z)
            case "z":
                return State(self.w, self.x, self.y, v)
            case _:
                raise KeyError(f"invalid state key {k}")

    def operate(self, op: t.Callable[[int, int], int], tgt: str, arg: str) -> State:
        return self.set(tgt, op(self[tgt], self[arg]))


def step(states: dict[State, int], instr: list[str]) -> tuple[bool, dict[State, int]]:
    cmd, tgt, *args = instr
    new_states: dict[State, int] = {}

    if cmd == "inp":
        assert not args
        for digit in range(1, 10):
            for state, val in states.items():
                assert not args
                new = state.set(tgt, digit)
                new_val = val * 10 + digit
                if new not in new_states:
                    new_states[new] = new_val
                new_states[new] = max(new_states[new], new_val)
    else:
        (arg,) = args
        op = ops[cmd]
        for state, val in states.items():
            new = state.operate(op, tgt, arg)
            if new not in new_states:
                new_states[new] = val
            new_states[new] = max(new_states[new], val)

    return cmd == "inp", new_states


def main():
    instrs = [line.strip().split() for line in sys.stdin]
    states = {State(0, 0, 0, 0): 0}
    inps = 0
    for i, instr in enumerate(instrs):
        inp, states = step(states, instr)
        inps += inp
        print(f"{len(states)} states after instruction {i} (at input {inps})")
    print(max(states.values()))


if __name__ == "__main__":
    main()
