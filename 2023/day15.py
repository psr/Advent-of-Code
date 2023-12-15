from functools import partial, reduce
import re


example = b"rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"

def hash_combine(c, n):
    return ((c + n) * 17) & 0xff

assert hash_combine(0, ord('H')) == 200

def part_1(input_):
    return sum(reduce(hash_combine, w, 0) for w in input_.rstrip().split(b',')) 

assert part_1(example) == 1320

with open('inputs/day15.txt', 'rb') as day15:
    print(f"{part_1(day15.read())=}")

hash_ = lambda bs: reduce(hash_combine, bs, 0)

step = re.compile(rb'(\w+)(-|=)(\d*)(?:,|\s*$)')

def box_sum(box_no, box):
    """the result of multiplying together:

    One plus the box number of the lens in question.
    The slot number of the lens within the box: 1 for the first lens, 2 for the second lens, and so on.
    The focal length of the lens.
    """
    focal_lengths = map(int, box.values())
    lenses = enumerate(focal_lengths, start=1)
    return sum(box_no * slot_no * focal_length for slot_no, focal_length in lenses)

def part_2(input_):
    boxes = [{} for _ in range(256)]
    for match in step.finditer(input_):
        label, command, length = match.groups()
        box = boxes[hash_(label)]
        match command:
            case b'-':
                box.pop(label, None)
            case b'=':
                box[label] = length
    return sum(box_sum(i, b) for i, b in enumerate(boxes, start=1))

assert part_2(example) == 145

with open('inputs/day15.txt', 'rb') as day15:
    print(f"{part_2(day15.read())=}")
