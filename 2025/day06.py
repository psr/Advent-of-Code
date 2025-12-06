import fileinput
from collections import defaultdict
from functools import reduce
from itertools import count, starmap
from operator import add, mul

example = """\
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +
""".splitlines(keepends=True)


def parse1(input_):
    rows = [line.strip().split() for line in input_]
    operators = rows.pop()
    parsed_rows = (map(int, r) for r in rows)
    columns = list(zip(*parsed_rows))
    return columns, operators


def test_parse1():
    assert parse1(example)[0][0] == (123, 45, 6)
    assert parse1(example)[1][0] == "*"


def do_column(column, operator):
    if operator == "+":
        initial = 0
        op = add
    elif operator == "*":
        initial = 1
        op = mul
    else:
        raise ValueError(operator)
    return reduce(op, column, initial)


def part_1(input_):
    parsed_input = parse1(input_)
    return sum(starmap(do_column, zip(*parsed_input)))


def test_part1_example():
    assert part_1(example) == 4277556


def parse2(input_):
    operators = input_.pop().split()  # assume it's a list
    numbers = defaultdict(int)
    for line in input_:
        for column, digit in enumerate(line):
            if not digit.isdigit():
                continue
            numbers[column] *= 10
            numbers[column] += int(digit)
    col_numbers = count()
    groups = []
    current = []
    while numbers:
        col_number = next(col_numbers)
        if col_number not in numbers:
            # blank column, end of group
            groups.append(current)
            current = []
            continue
        current.append(numbers.pop(col_number))
    groups.append(current)
    return groups, operators


def part_2(input_):
    parsed_input = parse2(input_)
    return sum(starmap(do_column, zip(*parsed_input)))


def test_part2_example():
    assert part_2(example) == 3263827


if __name__ == "__main__":
    with fileinput.input(mode="r", encoding="utf-8") as input_:
        day06 = list(input_)
        print(f"{part_1(day06)=}")
        print(f"{part_2(day06)=}")
