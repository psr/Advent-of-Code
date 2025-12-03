import fileinput
from functools import partial

example = """\
987654321111111
811111111111119
234234234234278
818181911112111
""".splitlines(keepends=True)


def parse(input_):
    return [[int(c) for c in line.strip()] for line in input_]


def find_largest_joltage(bank):
    battery_pairs = zip(bank, bank[1:])
    tens, units = next(battery_pairs)
    for left, right in battery_pairs:
        if tens < left:
            tens = left
            units = right
            continue
        if units < right:
            units = right
    return tens * 10 + units


def part_1(banks):
    return sum(find_largest_joltage(bank) for bank in banks)


def test_part1_example():
    assert part_1(parse(example)) == 357


def find_largest_joltage_many(n_batteries, bank):
    battery_windows = zip(*[bank[n:] for n in range(n_batteries)])
    best_batteries = list(next(battery_windows))
    for window in battery_windows:
        for i, battery in enumerate(window):
            if best_batteries[i] < battery:
                best_batteries[i:] = window[i:]
                continue
    return sum(b * 10**i for i, b in enumerate(reversed(best_batteries)))


def part_2(banks):
    find_largest_joltage_ = partial(find_largest_joltage_many, 12)
    return sum(find_largest_joltage_(bank) for bank in banks)


def test_part2_example():
    assert part_2(parse(example)) == 3121910778619


if __name__ == "__main__":
    with fileinput.input(mode="r", encoding="utf-8") as input_:
        day03 = parse(input_)
        print(f"{part_1(day03)=}")
        print(f"{part_2(day03)=}")
