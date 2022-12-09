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
DAY = 9


MOVEMENT = {
    'U': np.array([ 0,  1]),
    'D': np.array([ 0, -1]),
    'L': np.array([-1,  0]),
    'R': np.array([ 1,  0]),
}

def new_loc_counter():
    return collections.Counter([(0, 0)])

def update_move(head, tail, heading, steps, loc_counter=None):
    for _ in range(steps):
        head += MOVEMENT[heading]
        delta = head - tail
        if np.all(np.abs(delta) <= 1):
            continue
        tail += np.clip(delta, -1, 1)
        if loc_counter is not None:
            loc_counter.update([tuple(tail)])
        # print(tail)


def update_rope(rope, heading, steps, loc_counter):
    rope_len = len(rope)
    for _ in range(steps):
        rope[0] += MOVEMENT[heading]
        for h, t in zip(range(rope_len-1), range(1, rope_len)):
            delta = rope[h] - rope[t]
            if np.all(np.abs(delta) <= 1):
                continue
            rope[t] += np.clip(delta, -1, 1)
        loc_counter.update([tuple(rope[rope_len-1])])


def main():
    data = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""
    data = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""
    data = aocd.get_data(day=DAY, year=YEAR)
    inlist = [[h, int(i)] for h, i in (l.split() for l in data.split('\n'))]
    # print(inlist)

    head = np.zeros(2, dtype=np.int64)
    tail = head.copy()
    loc_counter = new_loc_counter()
    for heading, steps in inlist:
        update_move(head, tail, heading, steps, loc_counter)
        # print(head, tail)
    # print(len(loc_counter))
    answer = len(loc_counter)
    print(answer)
    # aocd.submit(answer, part='a', day=DAY, year=YEAR)

    rope = np.zeros((10, 2), dtype=np.int64)
    loc_counter = new_loc_counter()
    for heading, steps in inlist:
        update_rope(rope, heading, steps, loc_counter)
    answer = len(loc_counter)
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
