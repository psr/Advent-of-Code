from operator import itemgetter
from pathlib import Path
from itertools import chain, tee

input_path = Path(__file__).parent / '..' / 'inputs' / 'day6.txt'
with input_path.open('r', encoding='utf-8') as input_file:
    input_line = input_file.read()


def windowed(iterator, n):
    iterators = tee(iterator, n)
    for i in range(1, n):
        for iterator in iterators[i:]:
            next(iterator)
    return zip(*iterators)


def solve(input_line, n):
    windows = windowed(input_line, n)
    is_start = (len(set(w)) == n for w in windows)
    indexed = enumerate(is_start)
    only_valid = filter(itemgetter(1), indexed)
    i, _ = next(only_valid)
    return i + n


for i in range(4, len(input_line)):
    if len(set(input_line[i - 4: i])) < 4:
        continue
    print(i)
    break
else:
    print("Not found")


for i in range(14, len(input_line)):
    if len(set(input_line[i - 14: i])) < 14:
        continue
    print(i)
    break
else:
    print("Not found")


print(solve(input_line, 4))
print(solve(input_line, 14))
