import fileinput
from collections import defaultdict

example = """\
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
""".splitlines(keepends=True)


def parse(input_):
    input_ = (line.strip() for line in input_)
    start = next(input_).index("S")
    splitters = [{i for i, c in enumerate(line) if c == "^"} for line in input_]
    return start, splitters


def part_1(parsed_input):
    start, lines = parsed_input
    splits = 0
    beams = {start}
    for splitters in lines:
        splitters_hit = beams & splitters
        splits += len(splitters_hit)
        beams -= splitters_hit
        beams |= {s - 1 for s in splitters_hit}
        beams |= {s + 1 for s in splitters_hit}
    return splits


def test_part1_example():
    assert part_1(parse(example)) == 21


def part_2(parsed_input):
    start, lines = parsed_input
    timelines = defaultdict(int, {start: 1})
    for splitters in lines:
        # I feel like there's a better idiom for this, but I don't know it.
        splitters_hit = {s: timelines.pop(s) for s in timelines.keys() & splitters}
        for s, t in splitters_hit.items():
            timelines[s - 1] += t
            timelines[s + 1] += t
    return sum(timelines.values())


def test_part2_example():
    assert part_2(parse(example)) == 40


if __name__ == "__main__":
    with fileinput.input(mode="r", encoding="utf-8") as input_:
        day07 = parse(input_)
        print(f"{part_1(day07)=}")
        print(f"{part_2(day07)=}")
