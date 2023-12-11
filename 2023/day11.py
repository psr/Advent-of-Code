from functools import partial
from itertools import combinations, groupby, pairwise

example = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
""".splitlines(keepends=True)

example_expanded = """....#........
.........#...
#............
.............
.............
........#....
.#...........
............#
.............
.............
.........#...
#....#.......
""".splitlines(keepends=True)

def parse_galaxies(input_):
    for row, line in enumerate(input_):
        for col, c in enumerate(line):
            if c == '#':
                yield complex(col, row)
assert(len(list(parse_galaxies(example)))) == 9
assert(len(list(parse_galaxies(example_expanded)))) == 9
assert 3+0j in set(parse_galaxies(example))
assert 4+0j in set(parse_galaxies(example_expanded))

def expand_galaxies(galaxies, *, scale_direction, key, expand_amount=2):
    galaxies = sorted(galaxies, key=key)
    # Hack to avoid loosing groups when using pairwise
    grouped = groupby(galaxies, key)
    grouped = ((k, iter(list(g))) for k, g in grouped)

    shift_by = 0
    for (line1, galaxies1), (line2, galaxies2) in pairwise(grouped):
        yield from galaxies1  # Will already be exhausted except on first galaxies
        missing_lines = line2 - line1 - 1
        shift_by += missing_lines * (expand_amount - 1) * scale_direction
        yield from (g + shift_by for g in galaxies2)

expand_vertically = partial(expand_galaxies, scale_direction=1j, key=complex.imag.__get__)
expand_horizontally = partial(expand_galaxies, scale_direction=1, key=complex.real.__get__)

assert (set(
            expand_horizontally(
                expand_vertically(parse_galaxies(example))))
        == set(parse_galaxies(example_expanded)))

def manahattan_distance(c1, c2):
    difference = c1 - c2
    return int(abs(difference.real) + abs(difference.imag))

def part_1(input_, expand_amount=2):
    galaxies = parse_galaxies(input_)
    galaxies = expand_horizontally(galaxies, expand_amount=expand_amount)
    galaxies = expand_vertically(galaxies, expand_amount=expand_amount)
    galaxy_pairs = combinations(galaxies, 2)
    return sum(manahattan_distance(g1, g2) for g1, g2 in galaxy_pairs)

assert part_1(example) == 374, part_1(example)
assert part_1(example, expand_amount=10) == 1030
assert part_1(example, expand_amount=100) == 8410 

with open('inputs/day11.txt', 'r', encoding='utf-8') as input_:
    print(f"{part_1(input_)=}")

part_2 = partial(part_1, expand_amount=1_000_000)
with open('inputs/day11.txt', 'r', encoding='utf-8') as input_:
    print(f"{part_2(input_)=}")
