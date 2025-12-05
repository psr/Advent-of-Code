import fileinput
from itertools import groupby, takewhile

example = """\
3-5
10-14
16-20
12-18

1
5
8
11
17
32""".splitlines(keepends=True)


def parse(input_):
    input_ = (line.strip() for line in input_)
    bounds = (map(int, line.split("-")) for line in takewhile(bool, input_))
    ranges = [range(first, last + 1) for first, last in bounds]
    ingredients = [int(n) for n in input_]
    return ranges, ingredients


def part_1(parsed_input):
    ranges, ingredients = parsed_input

    def is_fresh(ingredient):
        return any(ingredient in r for r in ranges)

    return sum(is_fresh(i) for i in ingredients)


def test_part1_example():
    assert part_1(parse(example)) == 3


def part_2(parsed_input):
    ranges, _ = parsed_input
    # Sort ranges into order of endpoint, startpoint
    ranges = sorted(ranges, key=lambda r: (r.stop, r.start))
    # Groups of ranges that have the same end-point
    range_groups = groupby(ranges, key=range.stop.__get__)
    end_point, group = next(range_groups)
    # first-starting range that ends at this point
    current_range = next(group)
    total = 0
    for _, group in range_groups:
        first_range = next(group)
        if first_range.start <= current_range.start:
            # Starts as early or earlier, ends later, what's not to like?
            # This range subsumes our current range, so replaces it.
            current_range = first_range
            continue
        if first_range.start in current_range:
            # Overlapping ranges, build a new one.
            current_range = range(current_range.start, first_range.stop)
            continue
        # Non-overlapping range. Count the current range, and this
        # becomes current.
        total += len(current_range)
        current_range = first_range
    total += len(current_range)
    return total


def test_part2_example():
    assert part_2(parse(example)) == 14


if __name__ == "__main__":
    with fileinput.input(mode="r", encoding="utf-8") as input_:
        day05 = parse(input_)
        print(f"{part_1(day05)=}")
        print(f"{part_2(day05)=}")
