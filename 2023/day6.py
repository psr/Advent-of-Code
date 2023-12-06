import math
import re

example = """Time:      7  15   30
Distance:  9  40  200""".splitlines()

number = re.compile(r"\b(\d+)\b")

def parse_line(line):
    return (int(m.group(1)) for m in number.finditer(line))


assert list(parse_line(example[0])) == [7, 15, 30]


def parse_input(lines):
    lines = iter(lines)
    return zip(parse_line(next(lines)), parse_line(next(lines)))

assert list(parse_input(example)) == [(7,9), (15,40), (30, 200)]


def solve_1(time_allowed, record):
    target = record + 1  # Need to beat record
    discriminant = time_allowed ** 2 - 4 * target
    if discriminant < 0:
        return 0  # No roots, therefore no values that work
    assert discriminant != 0, "TODO"
    discriminant_sqrt = math.sqrt(discriminant)
    low = (time_allowed - discriminant_sqrt) / 2
    high = (time_allowed + discriminant_sqrt) / 2
    return math.floor(high) - math.ceil(low) + 1 

assert solve_1(7, 9) == 4
assert solve_1(15, 40) == 8
assert solve_1(30, 200) == 9
assert solve_1(71530, 940200) == 71503

def part_1(input_):
    return math.prod(solve_1(t, r) for t, r in parse_input(input_))

assert part_1(example) == 288, part_1(example)

with open('inputs/day6.txt', 'r', encoding='utf-8') as input_:
    print(f"{part_1(input_)=}")

# Can't be bother to parse properly, copy, paste, search, replace.
print(solve_1(49787980,298118510661181))