from itertools import groupby

example = """\
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
""".splitlines(keepends=True)


RIGHT = complex(1, 0)  # Increasing real
DOWN = complex(0, 1)  # Increasing imag
LEFT = -RIGHT  # Decreasing real
UP = -DOWN  # Decreasing imag


def parse(input_):
    input_ = (l.strip() for l in input_)
    return {
        RIGHT * x + DOWN * y: c
        for y, line in enumerate(input_)
        for x, c in enumerate(line)
    }


DIRECTIONS = [
    RIGHT,
    DOWN,
    LEFT,
    UP,
]


SYMBOLS = {
    LEFT: "→",
    RIGHT: "←",
    UP: "↑",
    DOWN: "↓",
}


def find_plot(grid, seed_coord, plant):
    plot = set()
    boundary = {seed_coord}
    while boundary:
        plot.update(boundary)
        boundary_neighbours = {c + d for c in boundary for d in DIRECTIONS}
        new_boundary = {n for n in boundary_neighbours if grid.get(n) == plant}
        for c in new_boundary:
            del grid[c]
        boundary = new_boundary
    return plot


def cost_fence_1(shape):
    area = len(shape)
    perimeter = sum(1 for c in shape for d in DIRECTIONS if c + d not in shape)
    return area * perimeter


def find_shapes(grid):
    while grid:
        seed_coord, plant = grid.popitem()
        yield find_plot(grid, seed_coord, plant)


def part_1(input_):
    grid = parse(input_)

    return sum(cost_fence_1(p) for p in find_shapes(grid))


assert part_1(example) == 1930


def count_edges(shape):
    # Urgh, this is going to be ugly
    # Create groups of boundary cells depending on which face is exposed
    groups = {d: {c for c in shape if c + d not in shape} for d in DIRECTIONS}
    # Then group things that are on the same row or column as appropriate
    get_row = lambda c: int(c.imag)
    get_col = lambda c: int(c.real)
    grouping_functions = {
        # If the left or right face is exposed we care about the
        # column they're on.
        LEFT: get_col,
        RIGHT: get_col,
        # For the up and down directions it's the row
        UP: get_row,
        DOWN: get_row,
    }
    adjacency_functions = {
        # If the left or right face is exposed,
        # cells are in the same edge if they have adjacent y coordinates.
        LEFT: get_row,
        RIGHT: get_row,
        # For up and down, the x coordinate
        UP: get_col,
        DOWN: get_col,
    }
    edge_count = 0
    for direction_exposed, exterior_cells in groups.items():
        # print(f"{SYMBOLS[direction_exposed]} {exterior_cells}")
        grouping_key = grouping_functions[direction_exposed]
        sorted_cells = sorted(exterior_cells, key=grouping_key)
        cell_groups = groupby(sorted_cells, key=grouping_key)
        for _, group in cell_groups:
            key = adjacency_functions[direction_exposed]
            # Extract the appropriate dimension from each coordinate
            # and sort into ascending order
            sorted_offsets = sorted(map(key, group))
            # Find contiguous subsequences and count them
            contiguous_subsequences = groupby(
                enumerate(sorted_offsets), lambda p: p[0] - p[1]
            )
            edge_count += sum(1 for _ in contiguous_subsequences)
    return edge_count


def cost_fence_2(shape):
    area = len(shape)
    sides = count_edges(shape)
    return area * sides


def part_2(input_):
    grid = parse(input_)

    return sum(cost_fence_2(p) for p in find_shapes(grid))


assert part_2(example) == 1206


if __name__ == "__main__":
    with open("inputs/day12.txt", "r", encoding="utf-8") as day12:
        print(f"{part_1(day12)=}")
    with open("inputs/day12.txt", "r", encoding="utf-8") as day12:
        print(f"{part_2(day12)=}")
