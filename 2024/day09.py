from collections import deque
from itertools import repeat, chain, islice, zip_longest

example = """\
2333133121414131402
""".splitlines(keepends=True)

def parse(input_):
    line, = (l.strip() for l in input_)
    return [(file_no, int(used), int(free) if free is not None else 0)
            for file_no, (used, free)
            in enumerate(zip_longest(line[::2], line[1::2]))]
assert parse(["12345"]) == [(0, 1, 2), (1, 3, 4), (2, 5, 0)]


def reorder_blocks_1(disk_map):
    backfill = chain.from_iterable(
        repeat(file_no, used_blocks)
        for file_no, used_blocks, _
        in reversed(disk_map))
    for file_no, used, free in disk_map:
        yield from repeat(file_no, used)
        yield from islice(backfill, free)


def part_1(input_):
    disk_map = parse(input_)
    total_blocks = sum(used for _file_no, used, _free in disk_map)
    reordered = islice(reorder_blocks_1(disk_map), total_blocks)
    return sum(block_no * file_no for block_no, file_no in enumerate(reordered))
assert part_1(example) == 1928


def reorder_blocks_2(disk_map):
    queue = deque(disk_map)
    while queue:
        file_no, used, free = queue.popleft()
        yield from repeat(file_no, used)
        if not free:
            continue
        rotation = 0
        max_rotation = len(queue)
        while rotation < max_rotation:
            moved_file_no, moved_used, moved_free = queue[-1]
            if moved_file_no is not None and moved_used <= free:
                queue.pop()
                yield from repeat(moved_file_no, moved_used)
                queue.append((None, moved_used, moved_free))
                free -= moved_used
            if not free:
                break
            rotation += 1
            queue.rotate()
        if rotation not in {0, max_rotation}:
            queue.rotate(-rotation)
        yield from repeat(None, free)
        while queue and queue[-1][0] is None:
            queue.pop()

def part_2(input_):
    disk_map = parse(input_)
    reordered = reorder_blocks_2(disk_map)
    return sum(block_no * file_no
               for block_no, file_no in enumerate(reordered)
               if file_no is not None)
assert part_2(example) == 2858


if __name__ == '__main__':
    with open('inputs/day09.txt', 'r', encoding='utf-8') as day09:
        print(f"{part_1(day09)=}")
    with open('inputs/day09.txt', 'r', encoding='utf-8') as day09:
        print(f"{part_2(day09)=}")
