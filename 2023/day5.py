from bisect import bisect, bisect_left, bisect_right

example = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4""".splitlines()

# Really don't have a good answer this morning

def parse_seeds(line:str):
    return [int(s) for s in line.split()[1:]]
assert parse_seeds(example[0]) == [79, 14, 55, 13]


def parse_map_line(line:str):
    dest, source, count = map(int, line.rstrip().split())
    source_range = range(source, source + count)
    return (source_range, dest - source)
assert parse_map_line("50 98 2\n") == (range(98, 100), -48)


def _map_key(pair):
    range, _ = pair
    return range.start


class RangeMapping:
    def __init__(self, parsed_lines):
        self._ranges, self._offsets = zip(*sorted(parsed_lines, key=_map_key))

    def __getitem__(self, value):
        index = bisect(self._ranges, value, key=range.start.__get__) - 1
        try:
            range_ = self._ranges[index]
        except IndexError:
            return value
        if value in range_:
            offset = self._offsets[index]
            return value + offset
        return value

assert RangeMapping(parse_map_line(l) for l in example[3:5])[50] == 52
assert RangeMapping(parse_map_line(l) for l in example[3:5])[1] == 1
assert RangeMapping(parse_map_line(l) for l in example[3:5])[100] == 100

from itertools import takewhile

def part_1(lines):
    lines = iter(lines)
    seeds = parse_seeds(next(lines))
    next(lines)  # Drop blank line
    for _ in lines:  # advance iterator over next title line? Should work?
        parsed_map_lines = (parse_map_line(l) for l in takewhile(lambda l: l and not l.isspace(), lines))
        mapping = RangeMapping(parsed_map_lines)
        seeds = [mapping[s] for s in seeds] 
    return min(seeds)

assert part_1(example) == 35

with open('inputs/day5.txt', 'r', encoding='utf-8') as input_:
    print(f"{part_1(input_)=}")


def parse_seed_ranges(line):
    numbers = iter(map(int, line.split()[1:]))
    return [range(start, start + count) for start, count in zip(numbers, numbers)]
        
assert parse_seed_ranges(example[0]) == [range(79, 79 + 14), range(55, 55 + 13)]


class RangeMapping2:
    def __init__(self, parsed_lines):
        self._ranges, self._offsets = zip(*sorted(parsed_lines, key=_map_key))

    def __getitem__(self, input_range):
        # assume that ranges are non-overlapping, therefore start of
        # one must be <= stop of previous.
        # Find ranges that could intersect with ours
        # Start with the first range who's stop point is after our start...
        start_index = bisect_right(self._ranges, input_range.start, key=range.stop.__get__)
        # ... and include ranges who's start is less than our stop
        relevant_ranges = takewhile(lambda r: r.start < input_range.stop, self._ranges[start_index:])
        # I'm pretty sure that's right, but it took AGES.

        relevant_offsets = self._offsets[start_index:]
        unmapped = input_range
        for range_to_map, offset in zip(relevant_ranges, relevant_offsets):
            if unmapped.start < range_to_map.start:
                partition_at = unmapped.index(range_to_map.start)
                yield unmapped[:partition_at]
                unmapped = unmapped[partition_at:]
            start = unmapped.start
            stop = min(range_to_map.stop, unmapped.stop)
            yield range(start + offset, stop + offset)
            if stop in unmapped:
                partition_at = unmapped.index(stop)
                unmapped = unmapped[partition_at:]
            else:
                unmapped = None  # If calculation above is correct won't cause issues
        if unmapped:
            yield unmapped


def part_2(lines):
    lines = iter(lines)
    seeds = parse_seed_ranges(next(lines))
    next(lines)  # Drop blank line
    for _ in lines:  # advance iterator over next title line? Should work?
        parsed_map_lines = (parse_map_line(l) for l in takewhile(lambda l: l and not l.isspace(), lines))
        mapping = RangeMapping2(parsed_map_lines)
        seeds = [r for s in seeds for r in mapping[s]]
    return min(seeds, key=range.start.__get__).start

assert part_2(example) == 46, part_2(example)

with open('inputs/day5.txt', 'r', encoding='utf-8') as input_:
    print(f"{part_2(input_)=}")
