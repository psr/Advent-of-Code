def parse_game(id_: int, line: str):
    game_id, game = line.split(':', 2)
    assert game_id == f"Game {id_}" 
    subsets = game.split(';')
    result = []
    for subset in subsets:
        cube_set = {}
        result.append(cube_set)
        for cube in subset.strip().split(","):
            n, colour = cube.lstrip().split(' ', 2)
            assert colour not in cube_set
            cube_set[colour] = int(n.lstrip())
        assert cube_set.keys() <= {'red', 'green', 'blue'}
    return result


example1 = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
""".splitlines()

assert parse_game(1, example1[0]) == [{'blue':3, 'red':4}, {'red':1,'green':2,'blue':6},{'green':2}]


cube_predicates = [
    lambda cube: cube.get('red', 0) <= 12,
    lambda cube: cube.get('green', 0) <= 13,
    lambda cube: cube.get('blue', 0) <= 14,
]

def is_valid_game(i, line):
    game = parse_game(i, line)
    return all(p(cubes) for cubes in game for p in cube_predicates)


def part_one_answer(input):
    return sum(i for i, l in enumerate(input, start=1) if is_valid_game(i, l))

assert(part_one_answer(example1)) == 8


with open('inputs/day2.txt', 'r', encoding='utf-8') as input_:
    print(f"{part_one_answer(input_)=}")