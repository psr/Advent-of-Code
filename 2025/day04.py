import fileinput

example = """\
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
""".splitlines(keepends=True)


def parse(input_):
    input_ = (line.strip() for line in input_)
    paper_rolls = set()
    for row, line in enumerate(input_):
        for col, c in enumerate(line):
            if c == "@":
                paper_rolls.add(complex(col, row))
    return frozenset(paper_rolls)


DIRECTIONS = {real + imag for real in [-1, 0, 1] for imag in [-1j, 0j, 1j]}
DIRECTIONS.discard(0 + 0j)


def neighbours(r):
    return {r + d for d in DIRECTIONS}


def is_accessible(paper_rolls, r):
    return len(neighbours(r) & paper_rolls) < 4


def part_1(paper_rolls):
    return sum(is_accessible(paper_rolls, r) for r in paper_rolls)


def test_part1_example():
    assert part_1(parse(example)) == 13


def part_2(paper_rolls):
    total = 0
    accessible = {r for r in paper_rolls if is_accessible(paper_rolls, r)}
    while accessible:
        total += len(accessible)
        paper_rolls -= accessible
        accessible = {r for r in paper_rolls if is_accessible(paper_rolls, r)}
    return total


def test_part2_example():
    assert part_2(parse(example)) == 43


if __name__ == "__main__":
    with fileinput.input(mode="r", encoding="utf-8") as input_:
        day04 = parse(input_)
        print(f"{part_1(day04)=}")
        print(f"{part_2(day04)=}")
