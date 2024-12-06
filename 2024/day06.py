from itertools import tee
from collections import defaultdict

example = """\
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
""".splitlines()

def find_obstacles(line):
    return (i for i, c in enumerate(line) if c == '#')

def find_start(line):
    if i := i.find('^') != -1:
        return i

def parse(input_):
    obstacles = frozenset()
    start = None
    for row, line in enumerate(input_):
        if start is None and (start_col := line.find('^')) != -1:
            start = start_col + row * -1j
        obstacles |= {i + row * -1j for i in find_obstacles(line)}
    width = len(line)
    height = row + 1
    return start, obstacles, width, height


def generate_path(position, direction, obstacles, width, height, extra_obstacle=None):
    while (0 <= position.real < width) and (0 >= position.imag > -height):
        yield position, direction  # We're entering position going direction
        next_pos = position + direction
        while next_pos in obstacles or next_pos == extra_obstacle:
            direction *= -1j  # Clockwise rotation
            next_pos = position + direction
        position = next_pos


def part_1(input_):
    position, obstacles, width, height = parse(input_)
    path = generate_path(position, 1j, obstacles, width, height)
    return len({p for p, d in path})
assert part_1(example) == 41



def part_2(input_):
    start, obstacles, width, height = parse(input_)
    path = generate_path(start, 1j, obstacles, width, height)
    path_history = {next(path)}  # Never place an obstacle on the start
    visited = {start}
    count = 0
    for position, direction in path:
        # What happens if we place an obstacle at position?
        if position in visited:
            continue
        new_path = generate_path(
            position - direction, direction * -1j, obstacles,
            width, height, extra_obstacle=position)
        new_history = set(path_history)
        for pair in new_path:
            if pair in new_history:
                count += 1
                break
            new_history.add(pair)
        path_history.add((position, direction))
        visited.add(position)
    return count
assert part_2(example) == 6

if __name__ == '__main__':
    with open('inputs/day06.txt', 'r', encoding='utf-8') as day06:
        print(f"{part_1(day06)=}")
    with open('inputs/day06.txt', 'r', encoding='utf-8') as day06:
        print(f"{part_2(day06)=}")
