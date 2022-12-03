import sympy

w, x, y, z = sympy.symbols("w x y z", integer=True)
syms = {"w": w, "x": x, "y": y, "z": z}


def parse() -> list[list[str]]:
    return [line.strip().split() for line in sys.stdin]


def reverse_eval(code: list[list[str]]):
    start = z
    get = lambda s: syms[s] if s in syms else int(s)
    for ins, first, *rest in code[::-1]:
        fs = syms[first]
        match ins:
            case "inp":
                pass
            case "add":
                start.subs(fs, fs + get(rest[0]))
            case "mul":
                start.subs(fs, fs * get(rest[0]))
            case "div":
                start.subs(fs, fs // get(rest[0]))
            case "mod":
                start.subs(fs, fs % get(rest[0]))
            case "eql":
                start.subs(fs, fs % get(rest[0]))
