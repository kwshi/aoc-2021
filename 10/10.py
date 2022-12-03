import collections as co
import functools as ft
import itertools as it
import operator as op
import sys

import numpy as np

matches = {")": "(", "]": "[", "}": "{", ">": "<"}
scores = {")": 3, "]": 57, "}": 1197, ">": 25137}
values = {"(": 1, "[": 2, "{": 3, "<": 4}


def parse(line):
    stack = []
    for c in line:
        if c in "([{<":
            stack.append(c)
            continue
        if not stack or matches[c] != stack[-1]:
            return scores[c], stack
        stack.pop()
    return 0, stack


def complete(stack):
    total = 0
    for c in stack[::-1]:
        total = total * 5 + values[c]
    return total


def main():
    lines = sys.stdin.read().split("\n")
    parsed = [*map(parse, lines)]
    print(sum(score for score, _ in parsed))

    stacks = [stack for score, stack in parsed if score == 0]
    stuff = sorted(map(complete, stacks))
    print(stuff[len(stuff) >> 1])


main()
