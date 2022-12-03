#!/usr/bin/env python3

# pylint: disable=invalid-name
# pylint: disable=missing-docstring
# pylint: disable=unspecified-encoding
# pylint: disable=unused-import
import aocd

YEAR = 2022
DAY = 1


def main():
    # data = aocd.get_data(day=DAY, year=YEAR)
    # inlist = data.split('\n')
    with open(f'input/{DAY:02d}.txt') as f:
        data = f.read()
    inlist = [[int(i) for i in l.split()] for l in data.split('\n\n')]

    print(max(map(sum, inlist)))

    l = list(map(sum, inlist))
    l.sort()
    print(sum(l[-3:]))

    # aocd.submit(answer, part='a', day=DAY, year=YEAR)

    # aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
