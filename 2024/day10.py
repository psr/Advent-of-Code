example = """\
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
""".splitlines(keepends=True)


def parse(input_):
    input_ = (l.strip() for l in input_)
    starts = set()
    grid = {}
    for row, line in enumerate(input_):
        for col, c in enumerate(line):
            coord = complex(col, row)
            if c == "0":
                starts.add(coord)
            grid[coord] = int(c) if c != "." else -1
    return starts, grid


directions = [
    complex(0, 1),
    complex(1, 0),
    complex(-1, 0),
    complex(0, -1),
]


def search_1(grid, coord, height):
    if height == 9:
        return {coord}
    next_height = height + 1
    neighbours = (coord + d for d in directions)
    valid_neighbours = (c for c in neighbours if grid.get(c) == next_height)
    results = (search_1(grid, n, next_height) for n in valid_neighbours)
    return set().union(*results)


def part_1(input_):
    startpoints, grid = parse(input_)
    return sum(len(search_1(grid, s, 0)) for s in startpoints)


assert part_1(example) == 36


def search_2(grid, coord, height):
    if height == 9:
        return 1
    next_height = height + 1
    neighbours = (coord + d for d in directions)
    valid_neighbours = (c for c in neighbours if grid.get(c) == next_height)
    return sum(search_2(grid, n, next_height) for n in valid_neighbours)


def part_2(input_):
    startpoints, grid = parse(input_)
    return sum(search_2(grid, s, 0) for s in startpoints)


assert part_2(example) == 81


if __name__ == "__main__":
    with open("inputs/day10.txt", "r", encoding="utf-8") as day10:
        print(f"{part_1(day10)=}")
    with open("inputs/day10.txt", "r", encoding="utf-8") as day10:
        print(f"{part_2(day10)=}")
