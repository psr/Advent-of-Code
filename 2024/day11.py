from collections import Counter
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


def count_stones(stones, blinks):
    stones = Counter(stones)
    for _ in range(blinks):
        next_stones = Counter()
        for stone, count in stones.items():
            left, right = blink(stone)
            next_stones[left] += count
            if right is not None:
                next_stones[right] += count
        stones = next_stones
    print(len(stones))
    return stones.total()


def part_1(input_):
    stones = parse(input_)
    return count_stones(stones, 25)


assert part_1(example) == 55312


def part_2(input_):
    stones = parse(input_)
    return count_stones(stones, 75)


if __name__ == "__main__":
    with open("inputs/day11.txt", "r", encoding="utf-8") as day11:
        print(f"{part_1(day11)=}")
    with open("inputs/day11.txt", "r", encoding="utf-8") as day11:
        print(f"{part_2(day11)=}")
