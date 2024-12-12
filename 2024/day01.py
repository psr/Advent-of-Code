import re
from collections import Counter

example_1 = """\
3   4
4   3
2   5
1   3
3   9
3   3
""".splitlines()

line_re = re.compile(r"^(\d+)\s+(\d+)$")


def parse_line(line):
    return map(int, line_re.match(line).groups())


assert list(parse_line(example_1[0])) == [3, 4]


def parse_input(input_):
    return zip(*(parse_line(l) for l in input_))


assert list(parse_input(example_1)) == [(3, 4, 2, 1, 3, 3), (4, 3, 5, 3, 9, 3)]


def abs_difference_pair(pair):
    x, y = pair
    return abs(x - y)


def part_1(input_):
    left, right = parse_input(input_)
    pairs_sorted = zip(sorted(left), sorted(right))
    return sum(abs_difference_pair(p) for p in pairs_sorted)


assert part_1(example_1) == 11


def part_2(input_):
    left, right = parse_input(input_)
    counts = Counter(right)
    return sum(counts[n] * n for n in left)


assert part_2(example_1) == 31


if __name__ == "__main__":
    with open("inputs/day01.txt", "r", encoding="utf-8") as day01:
        print(f"{part_1(day01)=}")
    with open("inputs/day01.txt", "r", encoding="utf-8") as day01:
        print(f"{part_2(day01)=}")
