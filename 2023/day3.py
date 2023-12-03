import math
import re
from collections import deque
from itertools import tee

example1 = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..""".splitlines()


number = re.compile(r'\d+')
symbol = re.compile(r'[^0-9.]')

assert len(number.findall(example1[0])) == 2
assert len(symbol.findall(example1[1])) == 1

def symbol_positions(line):
    return set(match.start() for match in symbol.finditer(line.strip()))

assert symbol_positions(example1[0]) == set()
assert symbol_positions(example1[1]) == {3}

def extract_numbers_from_line(line, symbols_in_surrounding_lines):
    for match in number.finditer(line):
        adjacent_indexes = set(range(match.start(), match.end())) | {match.start() - 1, match.end()}
        if any(adjacent_indexes & symbol_positions for symbol_positions in symbols_in_surrounding_lines):
            yield int(match.group())

assert list(
    extract_numbers_from_line(
        example1[0],
        [symbol_positions(example1[0]), symbol_positions(example1[1])])
    ) == [467]


# I'm sure there's a neater way of doing this
def make_windows(input_):
    input_ = iter(input_)
    queue = deque(maxlen=3)
    queue.append(next(input_))
    queue.append(next(input_))
    yield list(queue)
    for item in input_:
        queue.append(item)
        yield list(queue)
    queue.popleft()
    yield list(queue)
    
assert len(list(make_windows([1,2,3,4,5]))) == 5
assert list(make_windows([1,2,3,4,5])) == [[1,2], [1,2,3], [2,3,4], [3,4,5], [4,5]]


def part_1(input_):
    lines1, lines2 = tee(input_, 2)
    symbols = (symbol_positions(line) for line in lines1)
    windowed_symbol_positions = make_windows(symbols)
    # print(list(list(extract_numbers_from_line(l, s)) for l, s in zip(lines2, windowed_symbol_positions)))
    per_line_sums = (sum(extract_numbers_from_line(l, s)) for l, s in zip(lines2, windowed_symbol_positions))
    return sum(per_line_sums)

assert part_1(example1) == 4361


with open('inputs/day3.txt', 'r', encoding='utf-8') as input_:
    print(f"{part_1(input_)=}")


gear = re.compile(r'\*')

def number_matches(line):
    return [(range(m.start()-1, m.end() + 1), int(m.group())) for m in number.finditer(line)]

assert number_matches(example1[0]) == [(range(-1, 4), 467), (range(4, 9), 114)]

def find_gears(input_):
    lines1, lines2 = tee(input_, 2)
    numbers_for_lines = (number_matches(l) for l in lines1)
    windowed_number_matches = make_windows(numbers_for_lines)
    for line, window in zip(lines2, windowed_number_matches):
        for match in gear.finditer(line):
            matching_numbers = [n[1] for ns in window for n in ns if match.start() in n[0]]
            if len(matching_numbers) == 2:
                yield math.prod(matching_numbers)


def part_2(input_):
    return sum(find_gears(input_))

assert part_2(example1) == 467835

with open('inputs/day3.txt', 'r', encoding='utf-8') as input_:
    print(f"{part_2(input_)=}")
