import re
from itertools import count, groupby
from operator import itemgetter

example = """\
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
""".splitlines(keepends=True)

robot_re = re.compile(r"^p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)$")


def parse(input_):
    matches = (robot_re.match(line) for line in input_)
    numbers = (map(int, match.groups()) for match in matches)
    return (((p_x, p_y), (v_x, v_y)) for p_x, p_y, v_x, v_y in numbers)


def part_1(input_, width=101, height=103, seconds=100):
    robots = parse(input_)
    top_left, top_right, bottom_left, bottom_right = 0, 0, 0, 0
    center_x, center_y = width // 2, height // 2
    for p, v in robots:
        final_x = (p[0] + v[0] * seconds) % width
        final_y = (p[1] + v[1] * seconds) % height
        if final_x < center_x and final_y < center_y:
            top_left += 1
        elif final_x < center_x and final_y > center_y:
            bottom_left += 1
        if final_x > center_x and final_y < center_y:
            top_right += 1
        elif final_x > center_x and final_y > center_y:
            bottom_right += 1
    return top_left * top_right * bottom_left * bottom_right


assert part_1(example, width=11, height=7) == 12

by_x = itemgetter(0)
by_y = itemgetter(1)


def find_positions(robots, n, width, height):
    positions = [
        ((p[0] + v[0] * n) % width, (p[1] + v[1] * n) % height) for p, v in robots
    ]
    positions.sort(key=by_x)
    positions.sort(key=by_y)
    return positions


def display_positions(positions, width, height):
    print("\033[2J", end="")  # Clear screen
    print("\033[H", end="")  # Place cursor in top-left
    current_y = 0
    for y, chars in groupby(positions, by_y):
        assert y < height
        print("\n" * (y - current_y), end="")
        current_x = 0
        for x, _ in chars:
            assert x < width
            if x == current_x - 1:
                continue
            assert x >= current_x
            print(" " * (x - current_x), end="")
            print("#", end="")
            current_x = x + 1
        print()
        current_y = y + 1


def part_2(input_, width=101, height=103):
    robots = list(parse(input_))
    # for n in count(64, step=height):
    # for n in count(14, step=width):
    for n in count(7892, width * height):
        positions = find_positions(robots, n, width, height)
        display_positions(positions, width, height)
        print(n)
        print("Does this look like a tree (N/y)? ", end="")
        if input().strip().lower().startswith("y"):
            break
    return n


if __name__ == "__main__":
    with open("inputs/day14.txt", "r", encoding="utf-8") as day14:
        print(f"{part_1(day14)=}")
    with open("inputs/day14.txt", "r", encoding="utf-8") as day14:
        print(f"{part_2(day14)=}")
