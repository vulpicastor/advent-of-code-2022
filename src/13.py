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
DAY = 13

def cmp(a, b):
    return (a > b) - (a < b)

def my_cmp(a, b):
    # print(a, b)
    if isinstance(a, int) and isinstance(b, int):
        return cmp(a, b)
    if isinstance(a, int):
        a = [a]
    elif isinstance(b, int):
        b = [b]
    for x, y in zip(a, b):
        if (cmp_res := my_cmp(x, y)) == 0:
            continue
        return cmp_res
    return cmp(len(a), len(b))


def main():
    data = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""
    data = aocd.get_data(day=DAY, year=YEAR)
    inlist = [l.split() for l in data.split('\n\n')]
    # print(inlist)
    pairs = []
    packets = []
    for pair in inlist:
        new_p = []
        for packet in pair:
            print(f'a={packet}')
            loc = {}
            exec(f'a={packet}', {}, loc)
            new_p.append(loc['a'])
            packets.append(loc['a'])
        pairs.append(new_p)
    # print(pairs)

    result = list(itertools.starmap(my_cmp, pairs))
    # print(result)
    answer = np.sum(np.argwhere(np.array(result) < 0) + 1)
    # print(answer)
    # aocd.submit(answer, part='a', day=DAY, year=YEAR)

    packets.extend([[[2]], [[6]]])
    packets.sort(key=functools.cmp_to_key(my_cmp))
    for p in packets:
        print(p)
    answer = (packets.index([[2]]) + 1) * (packets.index([[6]]) + 1)
    # answer = 
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
