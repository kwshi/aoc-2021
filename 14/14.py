import collections as co
import re
import sys

def main():
    template, rules = sys.stdin.read().strip().split('\n\n')
    rules = {
        tuple(match[1]): match[2]
        for match in map(
            re.compile(r'([A-Z]{2}) -> ([A-Z])').fullmatch,
            rules.split('\n'),
        )
        if match is not None
    }

    counts = co.Counter(zip(template, template[1:]))
    for _ in range(40):
        new = co.Counter()
        for (a, b), ct in counts.items():
            if (a, b) in rules:
                c = rules[a, b]
                new[a, c] += ct
                new[c, b] += ct
            else:
                new[a, b] += ct
        counts = new

    overall = co.Counter()
    for (a, b), ct in counts.items():
        overall[a] += ct
        overall[b] += ct
    overall[template[0]] += 1
    overall[template[-1]] += 1

    print((max(overall.values()) - min(overall.values()))//2)


if __name__ == '__main__':
    main()
