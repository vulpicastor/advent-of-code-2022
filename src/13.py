#!/usr/bin/env python3

import functools
import itertools

import numpy as np
import aocd

YEAR = 2022
DAY = 13


def cmp(a, b):
    # Credit: Stack Overflow
    return (a > b) - (a < b)


def my_cmp(a, b):
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
    inlist = data.split()
    packets = []
    for p in inlist:
        loc = {}
        # Why write my own parser when Python already has one? :P
        exec(f'a={p}', {}, loc)  # pylint: disable='exec-used'
        packets.append(loc['a'])

    # Horrible iterator hack to take two items at a time.
    result = list(itertools.starmap(my_cmp, zip(*[iter(packets)]*2)))
    answer = np.sum(np.argwhere(np.array(result) < 0) + 1)
    print(answer)
    aocd.submit(answer, part='a', day=DAY, year=YEAR)

    # [How many [layers [of [nested [lists]]]] would [you] [like]]?
    # Yes.
    packets.extend([[[2]], [[6]]])
    packets.sort(key=functools.cmp_to_key(my_cmp))
    answer = (packets.index([[2]]) + 1) * (packets.index([[6]]) + 1)
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
