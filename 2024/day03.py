import re

example_1 = """\
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
""".splitlines()

mul_instruction_re = re.compile(r"mul\((\d+),(\d+)\)")


def parse_1(input_):
    matches = (m for l in input_ for m in mul_instruction_re.finditer(l))
    yield from ((a, b) for a, b in (map(int, m.groups()) for m in matches))


def part_1(input_):
    return sum(a * b for a, b in parse_1(input_))


assert part_1(example_1) == 161

example_2 = """\
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
""".splitlines()

tokens = [
    ("MUL", r"mul\((\d+),(\d+)\)"),
    ("START", r"do\(\)"),
    ("STOP", r"don\'t\(\)"),
]
token_re = re.compile("|".join(f"(?P<{name}>{spec})" for name, spec in tokens))


def parse_2(input_):
    matches = (m for l in input_ for m in token_re.finditer(l))
    enabled = True
    for match_ in matches:
        if match_.lastgroup == "START":
            enabled = True
        elif match_.lastgroup == "STOP":
            enabled = False
        elif enabled and match_.lastgroup == "MUL":
            mul_groups = mul_instruction_re.match(match_.group()).groups()
            a, b = map(int, mul_groups)
            yield (a, b)


def part_2(input_):
    return sum(a * b for a, b in parse_2(input_))


assert part_2(example_2) == 48

if __name__ == "__main__":
    with open("inputs/day03.txt", "r", encoding="utf-8") as day03:
        print(f"{part_1(day03)=}")
    with open("inputs/day03.txt", "r", encoding="utf-8") as day03:
        print(f"{part_2(day03)=}")
