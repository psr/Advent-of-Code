example = """\
""".splitlines(keepends=True)


def parse(input_):
    input_ = (l.strip() for l in input_)
    pass


def part_1(input_):
    parsed = parse(input_)
    pass


assert part_1(example) == ...

# def part_2(input_):
#     parsed = parse(input_)

# assert part_2(example) == ...


if __name__ == "__main__":
    with open("inputs/dayNN.txt", "r", encoding="utf-8") as dayNN:
        print(f"{part_1(dayNN)=}")
    # with open('inputs/dayNN.txt', 'r', encoding='utf-8') as dayNN:
    #     print(f"{part_2(dayNN)=}")
