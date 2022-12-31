#!/usr/bin/env python3

# pylint: disable=unused-import
import collections
import functools
import io
import itertools
import operator as op
import re
import timeit

import numpy as np
import aocd

YEAR = 2022
DAY = 25


NUMERAL = {
    '=': -2,
    '-': -1,
    '0': 0,
    '1': 1,
    '2': 2,
}
STRINGIFY = {v: k for k, v in NUMERAL.items()}


def snafu2int(s: str):
    n = 0
    pos = 1
    for c in reversed(s):
        n += pos * NUMERAL[c]
        pos *= 5
    return n


def int2snafu(n: int):
    places = []
    if n < 0:
        raise ValueError()
    if n == 0:
        return '0'
    while n > 0:
        n, rem = divmod(n, 5)
        if rem > 2:
            n += 1
            rem -= 5
        places.append(rem)
    return ''.join(STRINGIFY[i] for i in reversed(places))


def main():
    data = """1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122"""
    data = aocd.get_data(day=DAY, year=YEAR)
    inlist = [l for l in data.split('\n')]

    num_list = list(map(snafu2int, inlist))
    print(num_list)
    answer = int2snafu(sum(num_list))
    print(answer)
    aocd.submit(answer, part='a', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
