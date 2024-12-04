example = """\
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
""".splitlines()

def parse(input_):
    return list(zip(*(l.strip() for l in input_)))  # transpose so that we have [x][y] indexing
example_parsed = parse(example)

assert example_parsed[4][0] == 'X'

def generate_coords(x, y, x_step, y_step, length):
    if x_step:
        x_indexes = range(x, x + length * x_step, x_step)
    else:
        x_indexes = [x] * length
    if y_step:
        y_indexes = range(y, y + length * y_step, y_step)
    else:
        y_indexes = [y] * length
    return zip(x_indexes, y_indexes)
assert list(generate_coords(4, 0, 1, 1, 4)) == [(4, 0), (5, 1), (6, 2), (7, 3)]
assert [example_parsed[x][y] for x, y in generate_coords(4, 0, 1, 1, 4)] == ['X', 'M', 'A', 'S'], [example_parsed[x][y] for x, y in generate_coords(0, 4, 1, 1, 4)]
assert list(generate_coords(0, 0, 0, -1, 4)) == [(0,0), (0,-1), (0,-2), (0,-3)], list(generate_coords(0, 0, 0, -1, 4))
assert list(generate_coords(1, 9, -1, -1, 4)) == [(1,9), (0, 8), (-1, 7), (-2,6)], list(generate_coords(1, 9, -1, -1, 4))

        
def test_direction(grid, x, y, x_step, y_step, target='XMAS'):
    coords = generate_coords(x, y, x_step, y_step, len(target))
    try:
        return all(grid[x_][y_] == c for (x_, y_), c in zip(coords, target))
    except IndexError:
        return False
assert test_direction(example_parsed, 4, 0, 1, 1)
assert not test_direction(example_parsed, 0, 0, 1, 1)
assert not test_direction(example_parsed, 0, 0, 0, -1)


directions = {
    ((0, -1), '↑'),
    ((1, -1), '↗'),
    ((1, 0), '→'),
    ((1, 1), '↘'),
    ((0, 1), '↓'),
    ((-1, 1), '↙'),
    ((-1, 0), '←'),
    ((-1, -1), '↖'),
 }


def part_1(input_):
    parsed = parse(input_)
    count = 0
    width = len(parsed)
    height = len(parsed[0])
    for x in range(width):
        for y in range(height):
            for (x_step, y_step), symbol in directions:
                if x < 3 and x_step < 0:
                    continue  # Don't go over the left edge
                if x > width - 4 and x_step > 0:
                    continue
                if y < 3 and y_step < 0:
                    continue
                if y > height - 4 and y_step > 0:
                    continue
                
                result = test_direction(parsed, x, y, x_step, y_step)
                count += result
                if result: print(f"Found match at {(x,y)}, {symbol}")
    return count
assert part_1(example) == 18

def is_x_mas(grid, x, y):
    top_left = grid[x-1][y-1]
    top_right = grid[x+1][y-1]
    bottom_left = grid[x-1][y+1]
    bottom_right = grid[x+1][y+1]
    is_valid = lambda a, b: a == 'M' and b == 'S'
    is_valid_line = lambda a, b: is_valid(a, b) or is_valid(b, a)
    return (is_valid_line(top_left, bottom_right)
            and is_valid_line(bottom_left, top_right))

def part_2(input_):
    grid = parse(input_)
    width = len(grid)
    height = len(grid[0])
    possible_centres = (
        (x, y) for x in range(1, width - 1) for y in range(1, height - 1)
        if grid[x][y] == 'A'
    )
    return sum(is_x_mas(grid, x, y) for x, y in possible_centres)
assert part_2(example) == 9
    

if __name__ == '__main__':
    with open('inputs/day04.txt', 'r', encoding='utf-8') as day04:
        print(f"{part_1(day04)=}")
    with open('inputs/day04.txt', 'r', encoding='utf-8') as day04:
        print(f"{part_2(day04)=}")




