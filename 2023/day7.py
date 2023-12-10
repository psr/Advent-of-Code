from collections import Counter

example = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483""".splitlines()

scores = "23456789TJQKA"
from itertools import groupby
score_card = scores.index

score_hand = lambda h: tuple(sorted((len(list(g)) for k, g in  groupby(sorted(h))), reverse=True))
def score_hand(hand: str):
    c = Counter(hand)
    sorted(c.values(), reverse=True)

assert score_hand("QQQJA") == (3, 1, 1)
assert score_hand("KK677") == (2, 2, 1)

def parse_line(line):
    hand, bid = line.split()
    return hand, int(bid)

def score_line(parsed_line):
    hand, bid = parsed_line
    return (score_hand(hand), tuple(score_card(c) for c in hand))

def part_1(input_):
    parsed = (parse_line(l) for l in input_)
    ranked = enumerate(sorted(parsed, key=score_line), start=1)
    return sum(i * bid for i, (_, bid) in ranked)

assert part_1(example) == 6440

with open('inputs/day7.txt', 'r', encoding='utf-8') as input_:
    print(f"{part_1(input_)=}")


scores2 = "J23456789TQKA"
score_card2 = scores2.index

def score_hand2(hand):
    c = Counter(hand)
    jokers = c.pop('J', 0)
    rank = sorted(c.values(), reverse=True)
    if not rank:
        return [jokers]
    rank[0] += jokers
    return rank

def score_line2(parsed_line):
    hand, bid = parsed_line
    return (score_hand2(hand), tuple(score_card2(c) for c in hand))


def part_2(input_):
    parsed = (parse_line(l) for l in input_)
    ranked = enumerate(sorted(parsed, key=score_line2), start=1)
    return sum(i * bid for i, (_, bid) in ranked)

assert part_2(example) == 5905

with open('inputs/day7.txt', 'r', encoding='utf-8') as input_:
    print(f"{part_2(input_)=}")
