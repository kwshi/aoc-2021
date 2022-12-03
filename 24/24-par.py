import sys

import itertools as it
import operator as op


def parse(f: str) -> list[list[str]]:
    with open(f, "r") as r:
        return [line.strip().split() for line in r]


def evaluate(code: list[list[str]]):
    namespace: dict[str, set[int]] = {k: {0} for k in "wxyz"}

    def operate(f, a: str, b: str):
        bv = namespace[b] if b in namespace else {int(b)}
        namespace[a] = {f(ai, bi) for ai, bi in it.product(namespace[a], bv)}

    for i, (ins, *args) in enumerate(code):
        match ins:
            case "inp":
                assert len(args) == 1
                namespace[args[0]] = {*range(1, 10)}
            case "add":
                assert len(args) == 2
                operate(op.add, *args)
            case "mul":
                assert len(args) == 2
                operate(op.mul, *args)
            case "div":
                assert len(args) == 2
                operate(op.floordiv, *args)
            case "mod":
                assert len(args) == 2
                operate(op.mod, *args)
            case "eql":
                assert len(args) == 2
                operate(lambda a, b: int(a == b), *args)
        print(i, ins, args, namespace)
    return namespace["z"]


# def evaluate_conv(code: list[list[str]], nums: int):
#    return evaluate(code, [*map(int, str(nums))])
#

code = parse("in.txt")
print(evaluate(code))
# while True:
#    x = int(input())
#    print(evaluate_conv(code, x))
