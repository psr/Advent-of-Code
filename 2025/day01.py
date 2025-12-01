import fileinput
import itertools
import re
from functools import reduce

example = """\
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
""".splitlines(keepends=True)


LINE_RE = re.compile(r"^(L|R)(\d+)$")


def parse(input_):
    input_ = (l.strip() for l in input_)
    for line in input_:
        dir, count = LINE_RE.match(line).groups()
        yield int(count) * (1 if dir == "R" else -1)


def test_parse_example():
    assert list(parse(example)) == [-68, -30, 48, -5, 60, -55, -1, -99, 14, -82]


def add_mod_100(a, b):
    return (a + b) % 100


def part_1(parsed):
    positions = itertools.accumulate(parsed, add_mod_100, initial=50)
    return sum(not p for p in positions)


def test_part_1_example():
    assert part_1(parse(example)) == 3


def zero_crossings(acc, movement):
    prev_crossings, initial_position = acc

    complete_rotations, new_position = divmod(initial_position + movement, 100)
    crossings = abs(complete_rotations)
    # If we end on zero, and we've completed rotations, subtract one
    # so we don't double count
    crossings -= new_position == 0 and complete_rotations > 0
    # When we start at zero and go right, we still need to
    # count the fact that we started at zero.
    # Negative movements take care of themselves.
    crossings += initial_position == 0 and movement > 0
    return (prev_crossings + crossings, new_position)


def part_2(parsed):
    zeros, final_position = reduce(zero_crossings, parsed, (0, 50))
    return zeros + (final_position == 0)


def test_part_2_example():
    assert part_2(parse(example)) == 6


if __name__ == "__main__":
    with fileinput.input(mode="r", encoding="utf-8") as input_:
        day01 = list(parse(input_))
        print(f"{part_1(day01)=}")
        print(f"{part_2(day01)=}")
