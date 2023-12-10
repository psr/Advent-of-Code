example1 = """.....
.S-7.
.|.|.
.L-J.
.....
""".splitlines(keepends=True)

example1_complex = """
-L|F7
7S-7|
L|7||
-L-J|
L|-JF
""".splitlines(keepends=True)

example2 = """..F7.
.FJ|.
SJ.L7
|F--J
LJ...
""".splitlines(keepends=True)

example2_complex = """
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
""".splitlines(keepends=True)


# Using my favourite trick of using complex numbers as vectors
# Reals are EW, imaginary are NS
N,S,E,W = (0-1j),(0+1j), (1+0j), (-1+0j)

adjacency_mapping = {
'|': [N,S], # is a vertical pipe connecting north and south.
'-': [E,W], # is a horizontal pipe connecting east and west.
'L': [N,E], # is a 90-degree bend connecting north and east.
'J': [N,W], # is a 90-degree bend connecting north and west.
'7': [S,W], # is a 90-degree bend connecting south and west.
'F': [S,E], # is a 90-degree bend connecting south and east.
'.': [], # is ground; there is no pipe in this tile.
# Assume connected to all neighbours
'S': [N,S,E,W], # is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
}

assert len(set(tuple(v) for v in adjacency_mapping.values())) == len(adjacency_mapping)  # No duplicates!

def process_input(input_):
    # First pass, just find out what each cell wants to be connected to.
    cells = {}
    start = None
    for y, line in enumerate(input_):
        for x, char in enumerate(line.rstrip()):
            position = (x + y*1j)
            cells[position] = {position + connection for connection in adjacency_mapping[char]}
            if char == 'S':
                start = position
    # Not sure if this is useful, but remove connections that are not mutual.
    # Also remove cells with zero or one neighbours
    cells_to_remove = set()
    for position, neighbours in cells.items():
        to_remove = {n for n in neighbours if position not in cells.get(n, set())}
        neighbours.difference_update(to_remove)
        if len(neighbours) < 2:
            cells_to_remove.add(position)
    for c in cells_to_remove:
        del cells[c]
    assert start in cells
    return start, cells, x + 1, y + 1


def traverse_cells(start, cells):
    # At the start of the search we go into the start cells two neighbours
    visiting = cells[start]
    dont_return_to = {start}  # Don't traverse backwards
    count = 1
    # print(count, visiting)
    next_cells = {n for v in visiting for n in cells[v]} - dont_return_to
    while next_cells:
        dont_return_to = visiting
        visiting = next_cells
        count +=1
        # print(count, visiting)
        next_cells = {n for v in visiting for n in cells[v]} - dont_return_to
    return count
assert traverse_cells(*process_input(example1)[:2]) == 4
assert traverse_cells(*process_input(example1_complex)[:2]) == 4
assert traverse_cells(*process_input(example2)[:2]) == 8
assert traverse_cells(*process_input(example2_complex)[:2]) == 8

def part_1(input_):
    return traverse_cells(*process_input(input_)[:2])



with open('inputs/day10.txt', 'r', encoding='utf-8') as input_:
    print(f"{part_1(input_)=}")


is_vertical = {d for d in adjacency_mapping if N in adjacency_mapping[d] or S in adjacency_mapping[d]}


def traverse_cells2(start, cells):
    """Starting at start yield positions and the direction we are going when we cross them
    """
    # At the start of the search we go into the start cells two neighbours
    came_from, going_to = cells[start]
    visiting = start
    yield visiting, going_to - came_from
    came_from, visiting, going_to = visiting, going_to, sum(cells[going_to]) - visiting
    while start != visiting:
        yield visiting, going_to - came_from
        came_from, visiting, going_to = visiting, going_to, sum(cells[going_to]) - visiting
    

def part_2(input_):
    start, cells, w, h = process_input(input_)
    cells_in_loop = dict(traverse_cells2(start, cells))
    assert start in cells_in_loop
    # A cell is inside the loop if
    #  it is not part of the loop,
    #  and there are an odd number of vertical cell walls to the left of it.
    # However the number of vertical walls is tricky, F-J would count as one,
    # But L-J would count as two (or zero)
    # So do a sort of winding number thing. values of cells in loop are vectors
    # And so when we can add up the vertical component as a sort of winding number
    # Work from left to right, counting the number of cell walls to the left
    # We can ignore the top and bottom rows
    count = 0
    for y in range(h):
        winding_number = (0+0j)
        for x in range(w):
            position = (x + y*1j)
            try:
                winding_number += cells_in_loop[position]
            except KeyError:
                # if int(winding_number.imag) != 0:
                #     breakpoint()
                #     yield position
                count += int(winding_number.imag) != 0
    return count

example3 = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
""".splitlines(keepends=True)

assert part_2(example3) == 4


with open('inputs/day10.txt', 'r', encoding='utf-8') as input_:
    print(f"{part_2(input_)=}")
