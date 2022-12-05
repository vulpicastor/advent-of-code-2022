#!/usr/bin/env python3

import aocd

YEAR = 2022
DAY = 2

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


def main():
    data = """A Y
B X
C Z
"""
    # data = aocd.get_data(day=DAY, year=YEAR)
    inlist = [l.split() for l in data.split('\n') if l]

    answer = sum(score(*m) for m in inlist)
    print(answer)
    aocd.submit(answer, part='a', day=DAY, year=YEAR)

    answer = sum(score(a, STRATEGY[x][a]) for a, x in inlist)
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
