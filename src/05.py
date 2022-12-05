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
DAY = 5


def parse_move(s):
    m = re.match(r'move (\d+) from (\d+) to (\d+)', s)
    # print(m.group(1, 2 , 3))
    return int(m.group(1)), int(m.group(2)), int(m.group(3))

def do_move(stacks, move):
    n, fr, to = move
    for _ in range(n):
        stacks[to].append(stacks[fr].pop())
    return stacks

def do_move2(stacks, move):
    n, fr, to = move

    print(move)
    if len(stacks[fr]) < n:
        moved = stacks[fr][-n:]
        print(moved)
        raise ValueError(f'Insufficient crates on stack {fr}')
    moved = stacks[fr][-n:]
    stacks[to].extend(moved)
    stacks[fr] = stacks[fr][:-n]
    # for l in stacks[1:]:
        # print(''.join(l))
    print(fr, ''.join(stacks[fr]))
    print(to, ''.join(stacks[to]))
    

def main():
    data = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""
    data = aocd.get_data(day=DAY, year=YEAR)
    dock, moves = data.split('\n\n')
    moves = moves.split('\n')
    docka = np.array([list(l) for l in dock.split('\n')])
    stacks = [[c for c in l if c != ' '] for l in (docka[::-1, :].T)[1::4, 1:]]
    stacks.insert(0, [])
    # print(stacks)
    # print(moves[:10])
    # for _, m in zip(range(2), moves):
    for l in stacks[1:]:
        print(''.join(l))
    for m in moves:
        # if m:
            do_move2(stacks, parse_move(m))
    # inlist = [l for l in data.split('\n')]
    print(stacks)

    # answer = ''.join(s[-1] for s in stacks if s)
    # print(answer)
    # aocd.submit(answer, part='a', day=DAY, year=YEAR)

    answer = ''.join(s[-1] if s else ' ' for s in stacks[1:])
    print(answer)
    # answer = 
    # print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
