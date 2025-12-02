import fileinput
import math as maths
from functools import lru_cache, partial
from itertools import chain, filterfalse
from operator import contains

example = """\
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124
""".splitlines(keepends=True)


def parse(input_):
    input_ = (l.strip() for l in input_)
    for line in input_:
        for id_range in line.split(","):
            if not id_range:
                continue
            start, end = map(int, id_range.split("-"))
            yield range(start, end + 1)


def is_valid(n):
    as_text = str(n)
    split_point = len(as_text) // 2
    return as_text[:split_point] != as_text[split_point:]


def test_is_valid():
    assert not is_valid(22)
    assert is_valid(23)
    assert is_valid(101)
    assert is_valid(1)


def part_1(input_):
    parsed = parse(input_)
    return sum(filterfalse(is_valid, chain.from_iterable(parsed)))


def test_part1_example():
    assert part_1(example) == 1227775554


def count_digits(n):
    if not n:
        return 1
    return maths.floor(maths.log10(n)) + 1


@lru_cache
def find_possible_pattern_lengths(n_digits):
    # In many cases we can reduce the number of patterns to check,
    # avoiding work and double counting. For example, in a 12 digit
    # number any length-2 pattern repeated three times, is a length-6
    # pattern, so if we're going to check for all length-6 patterns
    # we're implicitly checking for all the length-2 patterns (and all
    # the length-3 patterns).
    #
    # This algorithm is horrible, and I feel bad about it.
    factors = set()
    implicit_factors = set()

    for f in range(n_digits // 2, 0, -1):
        if not n_digits % f and f not in implicit_factors:
            factors.add(f)
            for i in range(1, f // 2 + 1):
                if not f % i:
                    implicit_factors.add(i)
    return frozenset(factors)


def test_find_possible_pattern_lengths():
    assert find_possible_pattern_lengths(6) == {2, 3}
    assert find_possible_pattern_lengths(12) == {4, 6}
    assert find_possible_pattern_lengths(7) == {1}
    assert find_possible_pattern_lengths(2) == {1}
    assert find_possible_pattern_lengths(1) == set()


def spans_orders_of_magnitude(range_):
    return count_digits(range_[0]) != count_digits(range_[-1])


def test_spans_orders_of_magnitude():
    assert spans_orders_of_magnitude(range(5, 50))
    assert not spans_orders_of_magnitude(range(5, 10))


def split_range_into_orders_of_magnitude(range_):
    # Given a range that spans orders of magnitude, (i.e. different numbers of digits), split it into contiguous ranges which do not.
    # E.g. range(95, 115) would become [range(95, 100), range(100, 115)]
    while spans_orders_of_magnitude(range_):
        split_point = 10 ** count_digits(range_.start)
        yield range(range_.start, split_point, range_.step)
        range_ = range(split_point, range_.stop, range_.step)
    yield range_


def test_split_range_into_orders_of_magnitude():
    assert list(split_range_into_orders_of_magnitude(range(10))) == [range(10)]
    assert list(split_range_into_orders_of_magnitude(range(95, 115))) == [
        range(95, 100),
        range(100, 115),
    ]


def find_prefix(length, n_digits, n):
    suffix_mod = 10 ** (n_digits - length)
    suffix = n % suffix_mod
    return (n - suffix) // suffix_mod


def test_find_prefix():
    assert find_prefix(2, 5, 12345) == 12
    assert find_prefix(1, 4, 9876) == 9


def apply_pattern(pattern_length, n_digits, pattern):
    multiply_by = 10**pattern_length
    n = pattern
    n_length = pattern_length
    while n_length < n_digits:
        n *= multiply_by
        n += pattern
        n_length += pattern_length
    return n


def test_apply_pattern():
    assert apply_pattern(2, 6, 12) == 121212


def iter_invalid(range_):
    for range_ in split_range_into_orders_of_magnitude(range_):
        n_digits = count_digits(range_.start)
        pattern_lengths = find_possible_pattern_lengths(n_digits)
        for pattern_length in pattern_lengths:
            first_prefix = find_prefix(pattern_length, n_digits, range_[0])
            last_prefix = find_prefix(pattern_length, n_digits, range_[-1])
            patterns = range(first_prefix, last_prefix + 1)
            pattern_builder = partial(apply_pattern, pattern_length, n_digits)
            possible_invalid_values = map(pattern_builder, patterns)
            is_in_range = partial(contains, range_)
            yield from filter(is_in_range, possible_invalid_values)


def test_iter_invalid():
    assert set(iter_invalid(range(11, 23))) == {11, 22}
    assert set(iter_invalid(range(95, 115))) == {99, 111}
    assert set(iter_invalid(range(998, 1012))) == {999, 1010}
    assert set(iter_invalid(range(1188511880, 1188511890))) == {1188511885}
    assert set(iter_invalid(range(222220, 222224))) == {222222}
    assert set(iter_invalid(range(1698522, 1698528))) == set()
    assert set(iter_invalid(range(446443, 446449))) == {446446}
    assert set(iter_invalid(range(38593856, 38593862))) == {38593859}
    assert set(iter_invalid(range(565653, 565659))) == {565656}
    assert set(iter_invalid(range(824824821, 824824827))) == {824824824}
    assert set(iter_invalid(range(2121212118, 2121212124))) == {2121212121}


def part_2(input_):
    parsed = parse(input_)
    # The set here is so disappointing, I'd thought I'd prevented
    # double counting, but things like 222222 is both two applications
    # of a length three pattern and three applications of a length two pattern.
    invalid = chain.from_iterable(set(iter_invalid(r)) for r in parsed)
    return sum(invalid)


def test_part2_example():
    assert part_2(example) == 4174379265


if __name__ == "__main__":
    # with fileinput.input(mode="r", encoding="utf-8") as day02:
    #     print(f"{part_1(day02)=}")
    with fileinput.input(mode="r", encoding="utf-8") as day02:
        print(f"{part_2(day02)=}")
