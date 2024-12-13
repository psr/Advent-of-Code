import re
from fractions import Fraction
from itertools import groupby

example = """\
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
""".splitlines(keepends=True)

button_re = re.compile(r"Button [AB]: X\+(\d+), Y\+(\d+)")
prize_re = re.compile(r"Prize: X=(\d+), Y=(\d+)")


def parse(input_):
    input_ = (l.strip() for l in input_)
    groups = groupby(input_, bool)  # Groups of non-blank and blank lines
    for nonempty, group in groups:
        if not nonempty:
            continue
        a_line, b_line, prize_line = group
        a_x, a_y = map(int, button_re.match(a_line).groups())
        b_x, b_y = map(int, button_re.match(b_line).groups())
        prize_x, prize_y = map(int, prize_re.match(prize_line).groups())
        yield (a_x, a_y), (b_x, b_y), (prize_x, prize_y)


def solve(a, b, prize):
    (a_x, a_y), (b_x, b_y), (prize_x, prize_y) = a, b, prize
    # Rewriting the equation for the y coordinate to give a
    # results in a constant minus a multiple of b
    k = Fraction(prize_y, a_y)
    b_coefficient = Fraction(b_y, a_y)
    # Substituting a into the equation for the x coordinate finds b
    b = (prize_x - a_x * k) / (b_x - b_coefficient * a_x)
    if not b.is_integer():
        return
    # Substitute b into one of the equations to get a
    a = Fraction(prize_x - b_x * b, a_x)
    if not a.is_integer():
        return
    return int(a), int(b)


def part_1(input_):
    problems = parse(input_)
    solutions = (solve(*p) for p in parsed)
    valid_solutions = (s for s in solutions if s is not None)
    return sum(3 * a + b for a, b in valid_solutions)


assert part_1(example) == 480


def part_2(input_):
    offset = 10000000000000
    problems = parse(input_)
    problems_with_offsets = (
        (a, b, (p_x + offset, p_y + offset)) for a, b, (p_x, p_y) in parsed
    )
    solutions = (solve(*p) for p in problems)
    valid_solutions = (s for s in solutions if s is not None)
    return sum(3 * a + b for a, b in valid_solutions)


if __name__ == "__main__":
    with open("inputs/day13.txt", "r", encoding="utf-8") as day13:
        print(f"{part_1(day13)=}")
    with open("inputs/day13.txt", "r", encoding="utf-8") as day13:
        print(f"{part_2(day13)=}")
