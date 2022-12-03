import sys

import random


def parse(f: str) -> list[list[str]]:
    with open(f, "r") as r:
        return [line.strip().split() for line in r]


def evaluate(code: list[list[str]], nums: list[int]):
    inputs = iter(nums)
    namespace: dict[str, int] = {k: 0 for k in "wxyz"}
    for ins, *args in code:
        match ins:
            case "inp":
                assert len(args) == 1
                namespace[args[0]] = next(inputs)
            case "add":
                assert len(args) == 2
                a, b = args
                namespace[a] += namespace[b] if b in namespace else int(b)
            case "mul":
                assert len(args) == 2
                a, b = args
                namespace[a] *= namespace[b] if b in namespace else int(b)
            case "div":
                assert len(args) == 2
                a, b = args
                namespace[a] //= namespace[b] if b in namespace else int(b)
            case "mod":
                assert len(args) == 2
                a, b = args
                namespace[a] %= namespace[b] if b in namespace else int(b)
            case "eql":
                assert len(args) == 2
                a, b = args
                namespace[a] = int(
                    namespace[a] == (namespace[b] if b in namespace else int(b))
                )
        # print(namespace)
    return namespace["z"]


def evaluate_conv(code: list[list[str]], nums: int):
    return evaluate(code, [*map(int, str(nums))])


code = parse("in.txt")
while True:
    x = int(input())
    print(evaluate_conv(code, x))
