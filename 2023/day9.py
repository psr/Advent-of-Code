from functools import reduce
from itertools import pairwise
from operator import sub
import re


example = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
""".splitlines(keepends=True)

digits = re.compile(r'-?\d+')

parse_line = lambda l: [int(m) for m in digits.findall(l)]
assert parse_line(example[0]) == [0, 3, 6, 9, 12, 15]

def extrapolate(numbers):
    #print(numbers)
    if not any(numbers):
        return 0
    differences = [b - a for a, b in pairwise(numbers)]
    result = numbers[-1] + extrapolate(differences)
    return result

assert(extrapolate([0, 3, 6, 9, 12, 15])) == 18
assert(extrapolate(parse_line(example[1]))) == 28
assert(extrapolate(parse_line(example[2]))) == 68
extrapolate(parse_line("0 -1 -4 -12 -29 -43 6 276 1102 3136 7619 16928 35682 72975 146885 293622 586261 1173510 2360483 4776809 9723002"))

def part_1(input_):
    return sum(extrapolate(parse_line(l)) for l in input_)
assert part_1(example) == 114


with open('inputs/day9.txt', 'r', encoding='utf-8') as input_:
    print(f"{part_1(input_)=}")


def part_2(input_):
    return sum(extrapolate(parse_line(l)[::-1]) for l in input_)
assert part_2(example) == 2

with open('inputs/day9.txt', 'r', encoding='utf-8') as input_:
    print(f"{part_2(input_)=}")
