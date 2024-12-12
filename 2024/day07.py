from functools import reduce, partial
import operator
import math as maths


example = """\
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
""".splitlines()


def parse_line(l):
    target, numbers = l.split(":")
    return int(target), map(int, numbers.split())


def parse(input_):
    input_ = (l.strip() for l in input_)
    return (parse_line(l) for l in input_)


operations_1 = [
    operator.mul,
    operator.add,
]


def reducer(operations, target, accumulator, new_number):
    next_numbers = (
        operator(n, new_number) for operator in operations for n in accumulator
    )
    return {n for n in next_numbers if n <= target}


def solve(target, numbers, operations=operations_1):
    numbers = iter(numbers)
    initial_accumulator = {next(numbers)}
    reduction_function = partial(reducer, operations, target)
    final_numbers = reduce(reduction_function, numbers, initial_accumulator)
    return target in final_numbers


def part_1(input_):
    parsed = parse(input_)
    return sum(t for t, ns in parsed if solve(t, ns))


assert part_1(example) == 3749


def concat(n1, n2):
    if not n1:
        return n2
    n2_digits = maths.floor(maths.log10(n2)) + 1
    return n1 * (10**n2_digits) + n2


operations_2 = [
    operator.mul,
    operator.add,
    concat,
]


def part_2(input_):
    parsed = parse(input_)
    return sum(t for t, ns in parsed if solve(t, ns, operations=operations_2))


assert part_2(example) == 11387


if __name__ == "__main__":
    with open("inputs/day07.txt", "r", encoding="utf-8") as day07:
        print(f"{part_1(day07)=}")
    with open("inputs/day07.txt", "r", encoding="utf-8") as day07:
        print(f"{part_2(day07)=}")
