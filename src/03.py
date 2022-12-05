#!/usr/bin/env python3

import aocd

YEAR = 2022
DAY = 3


def priority(char):
    if char == '':
        return 0
    code = ord(char)
    if code > 96:
        return code - 96
    return code - 38


def split_half(line):
    idx = len(line) // 2
    return set(line[:idx]), set(line[idx:])


def intersect(*args):
    common = set(args[0])
    common.intersection_update(*[set(e) for e in args[1:]])
    if common:
        return common.pop()
    return ''


def main():
    data = aocd.get_data(day=DAY, year=YEAR)
    inlist = data.split('\n')

    answer = sum(priority(intersect(*split_half(l))) for l in inlist)
    print(answer)
    aocd.submit(answer, part='a', day=DAY, year=YEAR)

    n_group = len(inlist) // 3
    p_sum = 0
    for i in range(n_group):
        grouping = inlist[i*3:i*3+3]
        common = intersect(*grouping)
        p_sum += priority(common)
    print(p_sum)
    aocd.submit(p_sum, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
