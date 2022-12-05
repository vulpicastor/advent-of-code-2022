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
DAY = 4


def contains(a, b):
    a_lo, a_hi = a
    b_lo, b_hi = b
    if a_lo >= b_lo and a_hi <= b_hi:
        return True
    elif b_lo >= a_lo and b_hi <= a_hi:
        return True
    return False

def overlaps(a, b):
    if a[0] > b[0]:
        a, b = b, a
    if a[1] >= b[0]:
        return True
    return False

def main():
    data = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""
    data = aocd.get_data(day=DAY, year=YEAR)
    inlist = [[[int(i) for i in r.split('-')] for r in l.split(',')] for l in data.split('\n') if l]
    print(inlist)

    answer = sum(contains(a, b) for a, b in inlist)
    print(answer)

    # aocd.submit(answer, part='a', day=DAY, year=YEAR)

    answer = sum(overlaps(a, b) for a, b in inlist)
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
