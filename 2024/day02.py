example = b"""\
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
""".splitlines()

def parse_line(line):
    return [int(s) for s in line.split()]
assert parse_line(example[0]) == [7, 6, 4, 2, 1]


def parse(input_):
    return (parse_line(l) for l in input_)


def is_safely_ascending(a, b):
    return 0 < (b - a) < 4


def is_safely_descending(a, b):
    return 0 < (a - b) < 4


def is_safe_(predicate, report):
    pairs = zip(report, report[1:])
    return all(predicate(a, b) for a, b in pairs)


def is_safe(report):
    return (is_safe_(is_safely_ascending, report)
            or is_safe_(is_safely_descending, report))

def part_1(input_):
    return sum(is_safe(r) for r in parse(input_))
assert part_1(example) == 2


def scan_for_discontinuity(predicate, report):
    # Scan forward in the report, finding the first index where the
    # predicate doesn't hold
    for i, (a, b) in enumerate(zip(report, report[1:])):
        if not predicate(a, b):
            break
    else:
        return True
    left = i
    # Scan backwards in the report finding the last index where the
    # predicate doesn't hold
    for i, (a, b) in enumerate(zip(report[-2::-1], report[::-1]), start=2):
        if not predicate(a, b):
            break
    right = len(report) - i
    # Left and right each point at the first index of a pair which is
    # inconsistent with the rule.
    # What we do depends on the gap between them
    gap = right - left
    # If the gap is greater than one, there is no single element we can remove
    # to fix the inconsistency
    if gap > 1:
        return False
    # If the gap is one, there is only one element that can be removed to fix
    # the issue
    if gap == 1:
        return predicate(report[left], report[right + 1])
    # Otherwise the gap is zero (we found the same inconsistency in both passes)
    # and so we might be able to fix it by removing either the first or second
    # member of the inconsistent pair.
    # However we need to special case the start of the report
    assert left == right
    return (left == 0  # If the inconsistency is at the start, we can always fix
            or left == len(report) - 2 # Same for the end
            or predicate(report[left - 1], report[left + 1]) # Skip first
            or predicate(report[left], report[left + 2])) # Skip second
assert scan_for_discontinuity(is_safely_ascending, [1, 3, 2, 4, 5])
assert scan_for_discontinuity(is_safely_ascending, [1, 9, 2, 4, 5])
assert scan_for_discontinuity(is_safely_ascending, [9, 1, 2, 4, 5])
assert scan_for_discontinuity(is_safely_descending, [8, 6, 4, 4, 1])
assert scan_for_discontinuity(is_safely_ascending, [17, 19, 17, 20, 23])


def is_safe_tolerant(report):
    return (scan_for_discontinuity(is_safely_ascending, report)
            or scan_for_discontinuity(is_safely_descending, report))


def part_2(input_):
    return sum(is_safe_tolerant(r) for r in parse(input_))
assert part_2(example) == 4


if __name__ == '__main__':
    with open('inputs/day02.txt', 'rb') as day02:
        print(f"{part_1(day02)=}")
    with open('inputs/day02.txt', 'rb') as day02:
        print(f"{part_2(day02)=}")


