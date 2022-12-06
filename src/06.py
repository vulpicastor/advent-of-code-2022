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
DAY = 6



def marker(s, num_unique):
    for i in range(len(s) - num_unique + 1):
        if len(set(s[i:i+num_unique])) == num_unique:
            return i + num_unique
    return None


def main():
    data = """mjqjpqmgbljsphdztnvjfqwrcgsmlb
bvwbjplbgvbhsrlpgdmjqwftvncz
nppdvjthqldpwncqszvftbrmjlhg
nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg
zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"""
    inlist = [l for l in data.split('\n')]
    data = aocd.get_data(day=DAY, year=YEAR)

    print([marker(s, 4) for s in inlist])
    print([marker(s, 14) for s in inlist])

    answer = marker(data, 4)
    print(answer)
    aocd.submit(answer, part='a', day=DAY, year=YEAR)

    answer = marker(data, 14)
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
