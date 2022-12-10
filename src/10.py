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
DAY = 10



def emulate(prog):
    # cycle = 1
    rax = 1
    hist = [1]
    for ins in prog:
        match ins.split():
            case ['noop']:
                hist.append(rax)
                # cycle += 1
            case ['addx', n]:
                hist.append(rax)
                rax += int(n)
                hist.append(rax)
    return hist

def draw(hist):
    lines = []
    iterhist = iter(hist)
    while True:
        line = []
        for pos in range(40):
            try:
                rax = next(iterhist)
            except StopIteration:
                if line:
                    lines.append(''.join(line))
                return lines
            if pos in [rax-1, rax, rax+1]:
                line.append('#')
            else:
                line.append('.')
        lines.append(''.join(line))
            



def main():
    data = """noop
addx 3
addx -5"""
    data = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""
    data = aocd.get_data(day=DAY, year=YEAR)
    inlist = [l for l in data.split('\n')]

    hist = emulate(inlist)
    print([hist[i] for i in range(19, 221, 40)])
    answer = sum(i * hist[i-1] for i in range(20, 221, 40))
    print(answer)
    # aocd.submit(answer, part='a', day=DAY, year=YEAR)

    print(len(hist))
    [print(l) for l in draw(hist)]
    # answer = 
    # print(answer)
    # aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
