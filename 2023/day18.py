from itertools import cycle, tee
import re


example = """
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""

line_parts = re.compile(r'^([UDRL]) (\d+) \(#([0-9A-Fa-f]+)\)$', re.MULTILINE)
directions = {'U': -1j, 'D': 1j, 'L': -1+0j, 'R': 1+0j}

def parse(input_):
    for match in line_parts.finditer(input_):
        d, a, c = match.groups()
        yield directions[d], int(a), int(c, 16)

def interpret(instructions):
    position = 0+0j
    for direction, amount, _colour in instructions:
        yield from ((position := position + direction) for _ in range(amount))

assert len(set(interpret(parse(example)))) == 38
def find_edge_directions(edge_cells):
    # Like pairwise but for triplet-wise
    a, b, c = tee(edge_cells, 3)
    b, c = cycle(b), cycle(c)
    # Advance b and c
    next(b); next(c); next(c)
    for coming_from, on, going_to in zip(a, b, c):
        print(on, going_to - coming_from)
        yield (on, going_to - coming_from)
assert len(eg_dict := dict(find_edge_directions(interpret(parse(example))))) == 38
assert eg_dict[(0+0j)] == (1-1j), eg_dict[(0+0j)]

def find_bounds(cells):
    min_real, min_imag = float('inf'), float('inf')
    max_real, max_imag = float('-inf'), float('-inf')
    for cell in cells:
        min_real = min(min_real, cell.real)
        max_real = max(max_real, cell.real)
        min_imag = min(min_imag, cell.imag)
        max_imag = max(max_imag, cell.imag)
    return range(int(min_real), int(max_real) + 1), range(int(min_imag), int(max_imag) + 1)

def find_internal_cells(edge_cells):
    x_range, y_range = find_bounds(edge_cells)
    for y in y_range:
        winding = 0+0j
        for x in x_range:
            pos = complex(x, y)
            if not (dir := edge_cells.get(pos, None)):
                if winding.imag:
                    yield pos
                continue
            winding += dir
assert len(list(find_internal_cells(eg_dict))) + 38 == 62

def print_thing(data):
    x_range, y_range = find_bounds(data)
    for y in y_range:
        print(''.join('.#'[complex(x, y) in data] for x in x_range))


def part_1(input_):
    parsed = parse(input_)
    edge_cells = interpret(parsed)
    edge_directions = dict(find_edge_directions(edge_cells))
    internal_cells = list(find_internal_cells(edge_directions))
    assert not edge_directions.keys() & internal_cells
    print_thing(set(edge_directions) | set(internal_cells))
    return len(edge_directions) + len(set(internal_cells))
assert part_1(example) == 62



with open('inputs/day18.txt', 'r', encoding='utf-8') as input_:
    day18 = input_.read()

print(f"{part_1(day18)=}")

# print_thing(set(dict(interpret(parse(day18)))) | set(find_internal_cells(dict(interpret(parse(day18))))))

