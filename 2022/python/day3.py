from pathlib import Path

def priority(c):
    if 'a' <= c <= 'z':
        return ord(c) - ord('a') + 1
    if 'A' <= c <= 'Z':
        return ord(c) - ord('A') + 27
    raise ValueError(f'Out of range: {c}')


def find_duplicate(seq):
    split_point = len(seq) // 2
    compartment_a, compartment_b = seq[: split_point], seq[split_point :]
    (duplicate,) = set(compartment_a) & set(compartment_b)
    return duplicate


def find_common_item(elf1, elf2, elf3):
    (duplicate,) = (set(elf1) & set(elf2)) & set(elf3)
    return duplicate


input_path = Path(__file__).parent / '..' / 'inputs' / 'day3.txt'
with input_path.open('r', encoding='utf-8') as input_file:
    print(sum(priority(find_duplicate(l.strip())) for l in input_file))
with input_path.open('r', encoding='utf-8') as input_file:
    groups = zip(*[iter(l.strip() for l in input_file)] * 3)
    print(sum(priority(find_common_item(e1, e2, e3)) for e1, e2, e3 in groups))