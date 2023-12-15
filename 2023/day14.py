from functools import reduce
import functools
from itertools import count
from sys import intern


example = """\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
""".splitlines(keepends=True)

def parse(input_):
    lines = (l.rstrip() for l in input_)
    cols = zip(*lines)
    yield from (''.join(c) for c in cols)

parsed_example = [*parse(example)]
assert parsed_example[0] == "OO.O.O..##"

def combine(accumulator, input):
    score, first_free = accumulator
    position, char = input
    match (char):
        case 'O':
            # On encountering a rollable boulder
            # it rolls up to the first free space, which is what its score counts for
            # The new first_free value is the next value
            return (score + first_free), (first_free - 1)
        case '#':
            # On encountering a non-rollable boulder
            # The score is unchanged, but the first free position is now the next cell
            return score, (position - 1)
        case '.':
            # Take no action
            return accumulator

assert combine((0, 10), (10, 'O')) == (10, 9)

def solve_line(line):
    positions = range(1, len(line) + 1)[::-1]
    score, _ = reduce(combine, zip(positions, line), (0, positions[0]))
    return score

assert solve_line(parsed_example[0]) == 10 + 9 + 8 + 7

def part_1(input_):
    return sum(solve_line(l) for l in parse(input_))

assert part_1(example) == 136

with open('inputs/day14.txt', 'r', encoding='utf-8') as input_:
    print(f"{part_1(input_)=}")

@functools.cache
def tilt(line):
    parts = line.split('#')
    return '#'.join(''.join(sorted(p, reverse=True)) for p in parts)
assert tilt("OO.O.O..##") == "OOOO....##"


def rotate(grid):
    cols = zip(*grid)
    return tuple(''.join(c) for c in cols)[::-1]

assert rotate(("123", "456", "789")) == ("369", "258", "147")


def cycle(grid):
    for _ in range(4):
        grid = (tilt(line) for line in grid)
        grid = rotate(grid)
    return grid


assert (g :=cycle(parsed_example)) == tuple(parse(""".....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#....
""".splitlines(keepends=True)))
assert cycle(cycle(cycle(parsed_example))) == tuple(parse(""".....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#...O###.O
#.OOO#...O
""".splitlines(keepends=True)))

def part_2(input_):
    seen = {}
    grid = parse(input_)
    for n in count():
        cycle_start = seen.setdefault(grid, n)
        if cycle_start is not n:
            break
        grid = cycle(grid)
    cycle_length = n - cycle_start
    #print(f"{cycle_start=} {cycle_length=}")
    target_cycles = 1000000000
    cycles, to_do = divmod(target_cycles - cycle_start, cycle_length) 
    print(f"We have executed {cycle_start + cycle_length} cycles (equivalent to {cycles * cycle_length + cycle_start}). After {to_do} we will have done 1000000000")
    for _ in range(to_do):
        grid = cycle(grid)
    position_scores = range(1, len(grid[0]) + 1)[::-1]
    return sum(position_scores[i] for l in grid for i, c in enumerate(l) if c == 'O')

assert part_2(example) == 64, part_2(example)

with open('inputs/day14.txt', 'r', encoding='utf-8') as input_:
    print(f"{part_2(input_)=}")
