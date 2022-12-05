#!/usr/bin/env python3

import aocd

YEAR = 2022
DAY = 1


def main():
    data = aocd.get_data(day=DAY, year=YEAR)
    inlist = [[int(i) for i in l.split()] for l in data.split('\n\n')]

    answer = max(map(sum, inlist))
    print(answer)
    aocd.submit(answer, part='a', day=DAY, year=YEAR)

    l = list(map(sum, inlist))
    l.sort()
    answer = sum(l[-3:])
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
