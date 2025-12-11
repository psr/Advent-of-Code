import fileinput
from collections import defaultdict, deque, namedtuple

example1 = """\
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
""".splitlines(keepends=True)

node = namedtuple("node", ["incoming", "outgoing"])


def parse(input_):
    input_ = (line.strip() for line in input_)
    graph = defaultdict(lambda: node(set(), set()))
    for line in input_:
        name, destinations_s = line.split(":")
        destinations = destinations_s.split()
        graph[name].outgoing.update(destinations)
        for destination in destinations:
            graph[destination].incoming.add(name)
    return graph


def find_reachable(graph, start, *, restrict=None):
    if restrict is None:
        restrict = graph.keys()
    reachable = set()
    # BFS forwards, marking nodes as reachable
    queue = deque([start])
    while queue:
        key = queue.popleft()
        if key in reachable:
            continue
        reachable.add(key)
        queue.extend(graph[key].outgoing & restrict)
    return reachable


def find_reverse_reachable(graph, restrict, start):
    reachable = set()
    queue = deque([start])
    while queue:
        key = queue.popleft()
        if key in reachable:
            continue
        reachable.add(key)
        queue.extend(graph[key].incoming & restrict)
    return reachable


def count_paths(graph, reachable, start, end):
    assert start in reachable and end in reachable
    counts = {}
    # BFS backwards, counting paths
    queue = deque([end])
    while queue:
        key = queue.popleft()
        node = graph[key]
        if key in counts:
            continue
        unprocessed_downstream = node.outgoing & reachable - counts.keys()
        if unprocessed_downstream:
            # Delay processing this node until later.
            queue.extend(unprocessed_downstream)
            queue.append(key)
            continue
        reachable_upstream = node.incoming & reachable
        queue.extend(reachable_upstream)
        counts[key] = sum(counts[out] for out in node.outgoing & reachable) or 1
    return counts[start]


def part_1(graph):
    subgraph = find_reachable(graph, "you")
    return count_paths(graph, subgraph, "you", "out")


def test_part1_example():
    assert part_1(parse(example1)) == 5


example2 = """\
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
""".splitlines(keepends=True)


def part_2(graph):
    reachable_from_svr = find_reachable(graph, "svr")
    assert all(k in reachable_from_svr for k in {"svr", "dac", "fft", "out"})
    reachable_from_fft = find_reachable(graph, "fft", restrict=reachable_from_svr)
    # Maybe a worthwhile optimisation: The output is reachable from
    # the svr, dac and fft.  But either the dac is reachable from the
    # fft, or vice versa, but not both.  Otherwise there would be a
    # cycle, which we're presuming doesn't happen.
    if "dac" in reachable_from_fft:
        first_label, second_label = "fft", "dac"
        upstream_subgraph = reachable_from_fft
        downstream_subgraph = find_reachable(graph, "dac", restrict=reachable_from_fft)
    else:
        first_label, second_label = "dac", "fft"
        upstream_subgraph = find_reachable(graph, "dac", restrict=reachable_from_svr)
        downstream_subgraph = reachable_from_fft

    # Pretty sure this is unnecessary, but it fixes bugs in
    # count_paths(). The issue is with the requeuing, which needs to
    # know that the outgoing edges will / should be eventually
    # visited. I can't see a way to easily apply a proper fix in
    # there, so I'm just further restricting the nodes I visit to ones
    # that are definitely going to be on a path.
    subgraph1 = find_reverse_reachable(graph, reachable_from_svr, first_label)
    subgraph2 = find_reverse_reachable(graph, upstream_subgraph, second_label)
    subgraph3 = find_reverse_reachable(graph, downstream_subgraph, "out")

    paths1 = count_paths(graph, subgraph1, "svr", first_label)
    paths2 = count_paths(graph, subgraph2, first_label, second_label)
    paths3 = count_paths(graph, subgraph3, second_label, "out")
    return paths1 * paths2 * paths3


def test_part2_example():
    assert part_2(parse(example2)) == 2


if __name__ == "__main__":
    with fileinput.input(mode="r", encoding="utf-8") as input_:
        day11 = parse(input_)
        print(f"{part_1(day11)=}")
        print(f"{part_2(day11)=}")
