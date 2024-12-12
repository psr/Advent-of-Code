from collections import deque
from itertools import repeat, chain, islice, zip_longest

example = """\
2333133121414131402
""".splitlines(keepends=True)


def parse(input_):
    (line,) = (l.strip() for l in input_)
    return [
        (file_no, int(used), int(free) if free is not None else 0)
        for file_no, (used, free) in enumerate(zip_longest(line[::2], line[1::2]))
    ]


assert parse(["12345"]) == [(0, 1, 2), (1, 3, 4), (2, 5, 0)]


def reorder_blocks_1(disk_map):
    backfill = chain.from_iterable(
        repeat(f, used_blocks) for file_no, used_blocks, _ in reversed(disk_map)
    )
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
    left, right = 0, len(disk_map) - 1
    while left <= right:
        file_no, used, free = disk_map[left]
        yield from repeat(file_no, used)
        # Adjust right marker, tidying up after previous relocations
        while right > left and disk_map[right][0] is None:
            right -= 1
        # Can we fit anything into the free space?
        # Move downwards, yielding files which will fit,
        # leaving placeholders where we relocate files
        # and ignoring files which are already relocated.
        for index in range(right, left, -1):
            relocate_no, relocate_used, relocate_free = disk_map[index]
            if relocate_no is None:
                continue  # Already relocated
            if relocate_used <= free:
                # Relocate into current free space
                yield from repeat(relocate_no, relocate_used)
                free -= relocate_used
                # Leave a marker that this is has become empty.
                # Future rounds won't relocate this again,
                # but can relocate into the free space
                disk_map[index] = (None, relocate_used, relocate_free)
                continue
            if not free:
                break
        # Any remaining free space is unfillable
        yield from repeat(None, free)
        left += 1


# for n in reorder_blocks_2(parse(example)):
#     print(n if n is not None else '.', end='')
# print()


def part_2(input_):
    disk_map = parse(input_)
    reordered = reorder_blocks_2(disk_map)
    return sum(
        block_no * file_no
        for block_no, file_no in enumerate(reordered)
        if file_no is not None
    )


assert part_2(example) == 2858


if __name__ == "__main__":
    with open("inputs/day09.txt", "r", encoding="utf-8") as day09:
        print(f"{part_1(day09)=}")
    with open("inputs/day09.txt", "r", encoding="utf-8") as day09:
        print(f"{part_2(day09)=}")
