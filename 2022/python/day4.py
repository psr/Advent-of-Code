from pathlib import Path

def parse_line(line):
    left, right = line.strip().split(',')
    left_first, left_last = left.split('-')
    right_first, right_last = right.split('-')
    left_range = range(int(left_first), int(left_last) + 1)
    right_range = range(int(right_first), int(right_last) + 1)
    return left_range, right_range


def range_subset(left, right):
    """True if left is a proper subset of right"""
    return left.start in right and left.stop <= right.stop
    

def ranges_intersect(left, right):
    """True if there is any value in common between left and right"""
    return left.start in right or right.start in left


input_path = Path(__file__).parent / '..' / 'inputs' / 'day4.txt'
with input_path.open('r', encoding='utf-8') as input_file:
    section_assignments = [parse_line(l) for l in input_file]
print(sum(range_subset(l, r) or range_subset(r, l) for l, r in section_assignments))
print(sum(ranges_intersect(l, r) for l, r in section_assignments))
