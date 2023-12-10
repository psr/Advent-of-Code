example1 = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
""".splitlines(keepends=True)

example2 = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
""".splitlines(keepends=True)

from collections import defaultdict
from functools import reduce
from itertools import cycle, accumulate, dropwhile, takewhile, tee
import math
import re

line_pattern = re.compile(r'^(\w{3}) = \((\w{3}), (\w{3})\)\s*$')
def parse_line(line):
    node, left, right = line_pattern.match(line).groups()
    return node, (left, right)

def traverse_to(graph, start_node, directions, final_node_predicate):
    visited_nodes = accumulate(directions, lambda k, d: graph[k][d == 'R'], initial=start_node)
 #   print(list(islice(visited_nodes,0, 10)))
    i, n = next(dropwhile(lambda p: not final_node_predicate(p[1]), enumerate(visited_nodes)))
    return i

def part_1(input_):
    input_ = iter(input_)
    directions = cycle(next(input_).rstrip())
    next(input_)  # eat blank line
    graph = {n: d for n, d in (parse_line(l) for l in input_)}
    return traverse_to(graph, "AAA", directions, lambda n: n=="ZZZ")
    
#assert part_1(example1) == 2, part_1(example1)
assert part_1(example2) == 6

with open('inputs/day8.txt', 'r', encoding='utf-8') as input_:
    print(f"{part_1(input_)=}")

example3 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
""".splitlines(keepends=True)


def find_terminals_in_cycle(traversal, input_length):
    """"""
    terminals = defaultdict(list)
    only_terminals = filter(lambda p: p[1].endswith('Z'), traversal)
    cycle_found = False
    for offset, node in only_terminals:
        previous = terminals[node]
        # If we've seen this node before, was it an integer
        # number of input_lengths ago? If so we've found a
        # cycle
        for previous_count in previous:
            if (offset - previous_count) % input_length == 0:
                cycle_length = offset - previous_count
                cycle_offset = previous_count
                cycle_found = True
        if cycle_found:
            break
        else:
            previous.append(offset)
    terminals_on_run_in = sorted(offset for l in terminals.values() for offset in l if offset < cycle_offset)
    assert not terminals_on_run_in # Fix if needed
    terminals_on_loop = sorted(offset - cycle_offset for l in terminals.values() for offset in l if offset >= cycle_offset)
    assert terminals_on_loop # or we have a problem!
    return cycle_offset, cycle_length, terminals_on_loop

# This whole idea didn't work
def combine_cycles(cycle1, cycle2):
    off_1, l_1, t_1 = cycle1
    off_2, l_2, t_2 = cycle2
    new_cycle_length = math.lcm(l_1, l_2)
    l1_cycles_per_new_cycle = int(new_cycle_length / l_1)
    l2_cycles_per_new_cycle = int(new_cycle_length / l_2)
    
    # Find the first element that is in both cycles
    elements_1 = {off_1 + n * l_1 + o for o in t_1 for n in range(l1_cycles_per_new_cycle)}
    elements_2 = {off_2 + n * l_2 + o for o in t_2 for n in range(l2_cycles_per_new_cycle)}
    elements_both = elements_1 & elements_2
    offset = min(elements_both)
    new_cycle = sorted(e - offset for e in elements_both)
    return offset, new_cycle_length, new_cycle

def part_2(input_):
    input_ = iter(input_)
    directions = next(input_).rstrip()
    next(input_)  # eat blank line
    graph = {n: d for n, d in (parse_line(l) for l in input_)}
    start_nodes = [n for n in graph if n.endswith('A')]
    print(start_nodes)
    traversals = [enumerate(
                    accumulate(cycle(directions), lambda k, d: graph[k][d == 'R'], initial=s))
                  for s in start_nodes]
    cycle_info = [find_terminals_in_cycle(t, len(directions)) for t in traversals]
    # This seems to work for the data and the examples, but I think it would fail in other circumstances.
    return math.lcm(*(c[1] for c in cycle_info))

assert part_2(example3) == 6
with open('inputs/day8.txt', 'r', encoding='utf-8') as input_:
    print(f"{part_2(input_)=}")
