#!/usr/bin/env python3

import aocd

YEAR = 2022
DAY = 3


def priority(c):
    if c == '':
        return 0
    n = ord(c)
    if n > 96:
        return n - 96
    else:
        return n - 38


def intersect(l):
    idx = len(l) // 2
    first_half = set(l[:idx])
    second_half = set(l[idx:])
    if s := first_half & second_half:
        return s.pop()
    else:
        return ''


def intersect2(*args):
    s = set(args[0])
    s.intersection_update(*[set(e) for e in args[1:]])
    if s:
        return s.pop()
    else:
        return ''


def main():
    # data = aocd.get_data(day=DAY, year=YEAR)
    with open(f'input/{DAY:02d}.txt') as f:
        data = f.read()
    inlist = data.split('\n')

    print(sum(priority(intersect(l)) for l in inlist))

    n_group = len(inlist) // 3
    p_sum = 0
    for i in range(n_group):
        grouping = inlist[i*3:i*3+3]
        c = intersect2(*grouping)
        p_sum += priority(c)
    print(p_sum)

    # aocd.submit(answer, part='a', day=DAY, year=YEAR)

    # aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
