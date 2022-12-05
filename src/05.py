#!/usr/bin/env python3

import copy
import re

import numpy as np
import aocd

YEAR = 2022
DAY = 5


def parse_move(s):
    m = re.match(r'move (\d+) from (\d+) to (\d+)', s)
    return int(m.group(1)), int(m.group(2)), int(m.group(3))


def do_move(stacks, move):
    n, fr, to = move
    for _ in range(n):
        stacks[to].append(stacks[fr].pop())
    return stacks


def do_move2(stacks, move):
    n, fr, to = move
    stacks[to].extend(stacks[fr][-n:])
    del stacks[fr][-n:]
    

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
    # Horrible Numpy hack to transpose the input.
    stacks = [[c for c in l if c != ' '] for l in (docka[::-1, :].T)[1::4, 1:]]
    # I don't want to think about 1-indexing.
    stacks.insert(0, [])
    # Save a copy for part 2.
    stacks2 = copy.deepcopy(stacks)

    for m in moves:
        do_move(stacks, parse_move(m))
    answer = ''.join(s[-1] for s in stacks if s)
    print(answer)
    aocd.submit(answer, part='a', day=DAY, year=YEAR)

    stacks = stacks2
    for m in moves:
        do_move2(stacks, parse_move(m))
    answer = ''.join(s[-1] for s in stacks if s)
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
