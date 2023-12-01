import re
from pathlib import Path
from itertools import takewhile
import copy

diagram_line = re.compile(r'^\s*(?:\[[A-Z]\]\s*)+$')
move_line = re.compile(r'^move (\d+) from (\d+) to (\d+)')


def parse_diagram_line(l):
    cells = ((len(l) - 3) // 4) + 1
    return [l[4 * n + 1].strip() for n in range(cells)]


input_path = Path(__file__).parent / '..' / 'inputs' / 'day5.txt'
with input_path.open('r', encoding='utf-8') as input_file:
    _diagram_lines = takewhile(diagram_line.match, input_file)
    # Takewhile consumes the line with the column numbers.
    _parsed_lines = [parse_diagram_line(l) for l in _diagram_lines]
    crates = [[c for c in reversed(l) if c] for l in zip(*_parsed_lines)]
    next(input_file)  # Skip blank line.
    _movements = (move_line.match(line).groups() for line in input_file)
    movements = [[int(c), int(s) - 1, int(d) - 1] for c, s, d in _movements]


crates1 = copy.deepcopy(crates)
for count, src, dst in movements:
    for _ in range(count):
        crates1[dst].append(crates1[src].pop())
print(''.join([stack[-1] for stack in crates]))


crates2 = copy.deepcopy(crates)
for count, src, dst in movements:
    crates2[dst].extend(crates2[src][-count:])
    del crates2[src][-count:]
print(''.join([stack[-1] for stack in crates2]))