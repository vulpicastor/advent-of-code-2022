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

YEAR = 2021
DAY = 2



def win(a, x):
    match (a, x):
        case ('A', 'X') | ('B', 'Y') | ('C', 'Z'):
            return 3
        case ('A', 'Y') | ('B', 'Z') | ('C', 'X'):
            return 6
        case _:
            return 0
            
def score(a, x):
    s = ord(x) - 87
    return s + win(a, x)

STRATEGY = {
    'X': {
        'A': 'Z',
        'B': 'X',
        'C': 'Y',
    },
    'Y': {
        'A': 'X',
        'B': 'Y',
        'C': 'Z',
    },
    'Z': {
        'A': 'Y',
        'B': 'Z',
        'C': 'X',
    },
}

def main():
    # data = aocd.get_data(day=DAY, year=YEAR)
    data = """A Y
B X
C Z
"""
    with open(f'input/{DAY:02d}.txt') as f:
        data = f.read()
    inlist = [l.split() for l in data.split('\n')[:-1]]

    print(inlist)
    for m in inlist:
        print(m, score(*m))
    print(sum(score(*m) for m in inlist))

    total_score = 0
    for a, x in inlist:
        s = score(a, STRATEGY[x][a])
        total_score += s
        print(a, x, s)
    print(total_score)


    # aocd.submit(answer, part='a', day=DAY, year=YEAR)

    # aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
