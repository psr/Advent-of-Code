from functools import cache
from math import floor, log10

example = """\
125 17
""".splitlines(keepends=True)


def parse(input_):
    (line,) = (l.strip() for l in input_)
    return map(int, line.split())


def blink(stone):
    if not stone:
        return (1, None)
    digits = floor(log10(stone)) + 1
    if digits & 1:
        return (stone * 2024, None)
    return divmod(stone, 10 ** (digits // 2))


@cache
def count_stones(stone, blinks):
    if not blinks:
        return 1
    left, right = blink(stone)
    left_stones = count_stones(left, blinks - 1)
    right_stones = 0 if right is None else count_stones(right, blinks - 1)
    return left_stones + right_stones


def part_1(input_):
    stones = parse(input_)
    return sum(count_stones(s, 25) for s in stones)


assert part_1(example) == 55312


def part_2(input_):
    stones = parse(input_)
    return sum(count_stones(s, 75) for s in stones)


if __name__ == "__main__":
    with open("inputs/day11.txt", "r", encoding="utf-8") as day11:
        print(f"{part_1(day11)=}")
    with open("inputs/day11.txt", "r", encoding="utf-8") as day11:
        print(f"{part_2(day11)=}")
