from collections import defaultdict
from itertools import permutations, combinations, takewhile, accumulate, repeat
from math import gcd

example = """\
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
""".splitlines()

def parse(input_):
    input_ = (l.strip() for l in input_)
    antenae = defaultdict(list)
    for row, line in enumerate(input_):
        for col, c in enumerate(line):
            if c == '.':
                continue
            antenae[c].append(complex(col, row))
    width, height = col + 1, row+1
    return (width, height), antenae.values()


def find_antinodes_1(antanae):
    return (n1 - (n2 - n1) for n1, n2 in permutations(antanae, 2))


def part_1(input_):
    (width, height), antanae_for_frequencies = parse(input_)
    is_in_bounds = lambda antinode: (
        (0 <= antinode.real < width)
        and (0 <= antinode.imag < height))
    return len({n for antanae in antanae_for_frequencies
                for n in find_antinodes_1(antanae)
                if is_in_bounds(n)})
assert part_1(example) == 14


def find_antinodes_2(in_bounds, antanae):
    for n1, n2 in combinations(antanae, 2):
        difference = n2 - n1
        step = difference / gcd(int(difference.real), int(difference.imag))
        negative_steps = accumulate(repeat(-step))
        antinodes_before = (n1 + s for s in negative_steps)
        yield from takewhile(in_bounds, antinodes_before)
        yield n1
        positive_steps = accumulate(repeat(step))
        antinodes_after = (n1 + s for s in positive_steps)
        yield from takewhile(in_bounds, antinodes_after)


def part_2(input_):
    (width, height), antanae_for_frequencies = parse(input_)
    is_in_bounds = lambda antinode: (
        (0 <= antinode.real < width)
        and (0 <= antinode.imag < height))
    return len({n for antanae in antanae_for_frequencies
                for n in find_antinodes_2(is_in_bounds, antanae)})
assert part_2(example) == 34


if __name__ == '__main__':
    with open('inputs/day08.txt', 'r', encoding='utf-8') as day08:
        print(f"{part_1(day08)=}")
    with open('inputs/day08.txt', 'r', encoding='utf-8') as day08:
        print(f"{part_2(day08)=}")




