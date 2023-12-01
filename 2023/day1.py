import re

FIRST_DIGIT = re.compile(r'^\D*(\d)')
LAST_DIGIT = re.compile(r'(\d)\D*$')


def extract_calibration_value(line):
    d1 = FIRST_DIGIT.search(line).group(1)
    d2 = LAST_DIGIT.search(line).group(1)
    return int(f"{d1}{d2}")


EXAMPLES1 = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet""".splitlines()
EXPECTED_VALUES1 = [12, 38, 15, 77]
for e, r in zip(EXAMPLES1, EXPECTED_VALUES1):
    assert extract_calibration_value(e) == r, (e, r)


with open('inputs/day1.txt', 'r', encoding='utf-8') as input_:
    part1_answer = sum(extract_calibration_value(line) for line in input_)
print(f"Part 1 answer: {part1_answer}")


WORD_DIGITS = "one two three four five six seven eight nine".split()
FIRST_DIGIT_WORDS = re.compile(rf'^.*?(\d|{"|".join(WORD_DIGITS)})')
LAST_DIGIT_WORDS = re.compile(rf'^.*(\d|{"|".join(WORD_DIGITS)}).*?$')


def digit_to_int(d):
    return int(d) if d.isdigit() else WORD_DIGITS.index(d) + 1


def extract_calibration_value_words(line):
    d1 = digit_to_int(FIRST_DIGIT_WORDS.search(line).group(1))
    d2 = digit_to_int(LAST_DIGIT_WORDS.search(line).group(1))
    return 10 * d1 + d2


EXAMPLES2 = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen""".splitlines()
EXPECTED_VALUES2 = [29, 83, 13, 24, 42, 14, 76]
for e, r in zip(EXAMPLES2, EXPECTED_VALUES2):
    assert extract_calibration_value_words(e) == r, f"{e=} {extract_calibration_value_words(e)=} != {r}"


with open('inputs/day1.txt', 'r', encoding='utf-8') as input_:
    part2_answer = sum(extract_calibration_value_words(line) for line in input_)
print(f"Part 2 answer: {part2_answer}")