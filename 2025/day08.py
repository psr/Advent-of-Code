import fileinput
from heapq import nsmallest
from itertools import combinations, islice, starmap
from math import prod

example = """\
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
""".splitlines(keepends=True)


def parse(input_):
    input_ = (line.strip() for line in input_)
    return list(set(tuple(map(int, line.split(","))) for line in input_))


def squared_distance(a, b):
    return sum(starmap(lambda a, b: (a - b) ** 2, zip(a, b)))


class UnionFind:
    def __init__(self):
        self._parents = {}
        self._ranks = {}

    def find(self, node):
        parent = self._parents.setdefault(node, node)
        if parent != node:
            parent = self._parents[node] = self.find(parent)
        return parent

    def union(self, a, b):
        a_parent, b_parent = self.find(a), self.find(b)
        if a_parent == b_parent:
            return
        a_rank = self._ranks.pop(a_parent, 1)
        b_rank = self._ranks.pop(b_parent, 1)
        if a_rank >= b_rank:
            new_root = a_parent
            child = b_parent
        else:
            new_root = b_parent
            child = a_parent
        self._parents[child] = new_root
        self._ranks[new_root] = a_rank + b_rank


def by_distance(pair):
    return squared_distance(*pair)


def part_1(points, n_connections=1000):
    pairs = combinations(points, 2)
    uf = UnionFind()
    for a, b in nsmallest(n_connections, pairs, by_distance):
        uf.union(a, b)
    return prod(islice(sorted(uf._ranks.values(), reverse=True), 3))


def test_part1_example():
    assert part_1(parse(example), n_connections=10) == 40


def part_2(points):
    pairs = combinations(points, 2)
    uf = UnionFind()
    uf._ranks = {p: 1 for p in points}
    for a, b in sorted(pairs, key=by_distance):
        uf.union(a, b)
        if len(uf._ranks) == 1:
            return a[0] * b[0]


def test_part2_example():
    assert part_2(parse(example)) == 25272


if __name__ == "__main__":
    with fileinput.input(mode="r", encoding="utf-8") as input_:
        day08 = parse(input_)
        print(f"{part_1(day08)=}")
        print(f"{part_2(day08)=}")
