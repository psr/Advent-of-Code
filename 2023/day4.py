from collections import Counter

example1 = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11""".splitlines()

def parse_card(line: str):
    _card_number, rest = line.split(':', 2)
    winning, numbers = rest.split('|', 2)
    return {int(n.strip()) for n in winning.split()}, {int(n.strip()) for n in numbers.split()}

assert parse_card(example1[0]) == ({41, 48, 83, 86, 17}, {83, 86, 6, 31, 17, 9, 48, 53})

def score_card(card):
    winning, picked = card
    winning_count = len(winning & picked)
    return 1 << (winning_count - 1) if winning_count else 0


def part_1(lines):
    return sum(score_card(parse_card(l)) for l in lines)



with open('inputs/day4.txt', 'r', encoding='utf-8') as input_:
    print(f"{part_1(input_)=}")



def process_cards(cards):
    counter = Counter()
    for i, card in enumerate(cards):
        count_of_card = counter.pop(i, 0) + 1
        yield count_of_card
        winning, picked = card
        cards_won = len(winning & picked)
        next_card = i + 1
        cards_we_get_copies_of = range(next_card, next_card + cards_won)
        counter.update({c: count_of_card for c in cards_we_get_copies_of})

def part_2(lines):
    cards = (parse_card(l) for l in lines)
    return sum(process_cards(cards))

assert part_2(example1) == 30

with open('inputs/day4.txt', 'r', encoding='utf-8') as input_:
    print(f"{part_2(input_)=}")
