#!/usr/bin/env python3

import aocd

YEAR = 2022
DAY = 4


def contains(a, b):
    if a[0] <= b[0] and a[1] >= b[1]:
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

    answer = sum(contains(a, b) or contains(b, a) for a, b in inlist)  # pylint: disable=arguments-out-of-order
    print(answer)
    aocd.submit(answer, part='a', day=DAY, year=YEAR)

    answer = sum(overlaps(a, b) for a, b in inlist)
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
