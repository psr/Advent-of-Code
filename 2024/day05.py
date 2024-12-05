from collections import defaultdict
from itertools import takewhile, pairwise
from functools import cmp_to_key

example = """\
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
""".splitlines()

        
def parse(input_):
    input_ = (l.strip() for l in input_)
    rules = defaultdict(set)
    rules_lines = takewhile(lambda l:l, input_)
    for line in rules_lines:
        a, b = line.split('|', 2)
        rules[int(a)].add(int(b))
    update_lines = (
        [int(s) for s in l.split(',')] for l in input_)
    return rules, update_lines


def is_sorted(rules, update):
    consecutive_pairs = pairwise(update)
    return all(b in rules[a] or a not in rules[b] for a, b in consecutive_pairs)


def part_1(input_):
    rules, updates = parse(input_)
    valid_updates = filter(lambda u: is_sorted(rules, u), updates)
    middle_elements = (u[len(u)//2] for u in valid_updates)
    return sum(middle_elements)
assert part_1(example) == 143


def make_cmp_pages(rules):
    def cmp_pages(a, b):
        if b in rules[a]:
            return -1
        if a in rules[b]:
            return 1
        return 0
    return cmp_pages


def part_2(input_):
    rules, updates = parse(input_)
    invalid_updates = filter(lambda u: not is_sorted(rules, u), updates)
    key = cmp_to_key(make_cmp_pages(rules))
    sorted_updates = (sorted(u, key=key) for u in invalid_updates)
    middle_elements = (u[len(u)//2] for u in sorted_updates)
    return sum(middle_elements)
assert part_2(example) == 123
    

if __name__ == '__main__':
    with open('inputs/day05.txt', 'r', encoding='utf-8') as day05:
        print(f"{part_1(day05)=}")
    with open('inputs/day05.txt', 'r', encoding='utf-8') as day05:
        print(f"{part_2(day05)=}")




