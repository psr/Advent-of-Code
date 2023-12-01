from itertools import chain
from pathlib import Path


sample = """\
30373
25512
65332
33549
35390
""".splitlines()

def parse(input_):
    input_ = iter(input_)
    trees = [int(c) for c in next(input_).strip()]
    width = len(trees)
    trees.extend([int(c) for line in input_ for c in line.strip()])
    height = len(trees) // width
    return (width, height), trees


def right(trees, width, height, col, row):
    start = row * width + col + 1
    stop = (row + 1) * width
    return trees[start : stop : 1]

def left(trees, width, height, col, row):
    start = row * width + col - 1
    stop = row * width - 1
    return trees[start : stop : -1]

def up(trees, width, height, col, row):
    start = (row - 1) * width + col
    stop = col - 1
    return trees[start : stop : -width]

def down(trees, width, height, col, row):
    start = (row + 1) * width + col
    stop = (height - 1) * width + col + 1
    return trees[start : stop : width]

(width, height), trees = parse(sample)
assert (width, height) == (5, 5)
assert right(trees, width, height, 2, 2) == [3, 2], right(trees, width, height, 2, 2)
assert left(trees, width, height, 2, 2) == [5, 6], left(trees, width, height, 2, 2)
assert up(trees, width, height, 2, 2) == [5, 3]
assert down(trees, width, height, 2, 2) == [5, 3]

lines_of_sight = [up, down, left, right]

def is_visible(trees, width, height, row, col):
    tree = trees[row * width + col]
    lines = [d(trees, width, height, row, col) for d in lines_of_sight]
    return any(all(t < tree for t in line) for line in lines)

assert is_visible(trees, width, height, 1, 1)
assert not is_visible(trees, width, height, 1, 3)

assert sum(is_visible(trees, width, height, row, col) for row in range(height) for col in range(width)) == 21


input_path = Path(__file__).parent / '..' / 'inputs' / 'day8.txt'
with input_path.open('r', encoding='utf-8') as input_file:
    (width, height), trees = parse(input_file)
    print(sum(is_visible(trees, width, height, row, col) for row in range(height) for col in range(width)))

