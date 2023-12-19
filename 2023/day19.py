from copy import copy
from itertools import compress, takewhile
from math import prod
import re


example = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
""".splitlines(keepends=True)

workflow = re.compile(r'^(\w+)\{(.+),(\w+)\}$')
rule = re.compile(r'([xmas])([<>])(\d+):(.+?)(?:,|$)')
part_rating = re.compile(r'([xmas])=(\d+)(?:,|$)')
part_ratings = re.compile(r"^\{(.+)\}$")

def parse_rules(rules):
    for rule_match in rule.finditer(rules):
        property_, operator, quantity, destination = rule_match.groups()
        yield property_, operator, int(quantity), destination


def parse_workflow(line):
    name, rules, default = workflow.match(line).groups()
    return name, ([*parse_rules(rules)], default)

def parse_part_ratings(line):
    return {m.group(1): int(m.group(2)) for m in part_rating.finditer(part_ratings.match(line).group(1))}

def parse(input_):
    input_ = iter(input_)
    workflows = dict(parse_workflow(l) for l in takewhile(workflow.match, input_))
    parts = [parse_part_ratings(l) for l in takewhile(part_ratings.match, input_)]
    return workflows, parts

(example_workflows, example_parts) = parse(example)
assert len(example_workflows) == 11, example_workflows
assert len(example_parts) == 5, example_parts

def apply_rule(property_, operator, quantity, part):
    value = part[property_]
    match operator:
        case '<':
            return value < quantity
        case '>':    
            return value > quantity
    assert False, "Shouldn't get here"


def interpret_simple(workflows, part):
    workflow = 'in'
    while workflow not in {'R', 'A'}:
        rules, default = workflows[workflow]
        results = (apply_rule(p, o, q, part) for p, o, q, _d in rules)
        destinations = (d for _p, _o, _q, d in rules)
        workflow = next(compress(destinations, results), '') or default
    return workflow

assert [interpret_simple(example_workflows, p) for p in example_parts] == ['A','R','A','R','A']

def part_1(input_):
    workflows, parts = parse(input_)
    accepted_parts = (p for p in parts if interpret_simple(workflows, p) == 'A')
    return sum(v for p in accepted_parts for v in p.values())

assert part_1(example) == 19114


with open('inputs/day19.txt', 'r', encoding='utf-8') as day19:
    print(f"{part_1(day19)=}")

def slice_range(range_, operator, value):
    if operator == '<':
        if value in range_:
            index = range_.index(value)
            return range_[:index], range_[index:]
        if value < range_.start:
            return range(0,0), range_
        return range_, range(0,0)
    if operator == '>':
        value += 1
        if value in range_:
            index = range_.index(value)
            return range_[index:], range_[:index]
        if value < range_.start:
            return range_, range(0,0)
        return range(0,0), range_
assert slice_range(range(3,11), '<', 5) == (range(3, 5), range(5, 11))
assert slice_range(range(3,11), '>', 5) == (range(6, 11), range(3, 6))
assert slice_range(range(3,11), '<', 3) == (range(0), range(3, 11))
assert slice_range(range(3,11), '<', 11) == (range(3,11), range(0))


def slice_part(rule, part):
    """Given a rule, return the part that meets the rule, and the part that does not"""
    property_, operator, quantity, destination = rule
    range_ = part[property_]
    taken, left = slice_range(range_, operator, quantity)
    d1, d2 = copy(part), copy(part)  # I know there's a clever way to do this, but can never remember
    d1[property_] = taken
    d2[property_] = left
    return destination, d1, d2


def interpret_ranges(workflows, part, workflow='in'):
    if workflow == 'R':
        return
    if not all(part.values()):
        return
    if workflow == 'A':
        yield part
        return
    rules, default = workflows[workflow]
    for rule in rules:
        destination, taken, part = slice_part(rule, part)
        yield from interpret_ranges(workflows, taken, destination)
    yield from interpret_ranges(workflows, part, default)

initial_range = range(1, 4001)
initial_part = {p: initial_range for p in 'xmas'}

assert sum(prod(len(r) for r in d.values()) for d in interpret_ranges(example_workflows, initial_part)) == 167409079868000

def part_2(input_):
    workflows, _ = parse(input_)
    return sum(prod(len(r) for r in d.values()) for d in interpret_ranges(workflows, initial_part))

assert(part_2(example)) == 167409079868000

with open('inputs/day19.txt', 'r', encoding='utf-8') as day19:
    print(f"{part_2(day19)=}")