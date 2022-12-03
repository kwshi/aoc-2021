import sympy
import pprint as pp
import sys


def parse() -> list[list[str]]:
    return [line.strip().split() for line in sys.stdin]


inputs = sympy.symbols([f"x{i}" for i in range(14)], integer=True)


def evaluate(code: list[list[str]]):
    namespace: dict[str, int] = {k: 0 for k in "wxyz"}
    nums = iter(inputs)
    for ins, *args in code:
        match ins:
            case "inp":
                assert len(args) == 1
                namespace[args[0]] = next(nums)
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
                namespace[a] = sympy.KroneckerDelta(
                    namespace[a], (namespace[b] if b in namespace else int(b))
                )
        print(ins, args, namespace)
        print()
    return namespace["z"].simplify()


code = parse()
result = evaluate(code)


def run(n: int):
    return result.subs({sym: k for sym, k in zip(inputs, map(int, str(n)))})


pp.pprint(result.args)
print()

# print(evaluate(code).subs())
print(run(99999999999999))
