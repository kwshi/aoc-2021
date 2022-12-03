import sys


def decompile_step(instrs: list[list[str]], i: int) -> tuple[str, int]:
    match instrs[i]:
        case ["mul", "x", "0"] if instrs[i + 1 : i + 3] == [
            ["add", "x", "z"],
            ["mod", "x", "26"],
        ]:
            match instrs[i + 3]:
                case ["div", "z", "26"]:
                    return "x = pop(z)", 4
                case _:
                    print(instrs[i + 3])
                    return "x = peek(z)", 3

        case ["div", _, "1"]:
            return "", i + 1

        case ["mul", var, "0"] if instrs[i + 1][:2] == ["add", var]:
            return f"{var} = {instrs[i+1][2]}", i + 2

        case _:
            return " ".join(instrs[i]), i + 1


def decompile(instrs: list[list[str]]):
    i = 0
    while i < len(instrs):
        line, i = decompile_step(instrs, i)
        print(line)


instrs = [line.strip().split() for line in sys.stdin]
decompile(instrs)
