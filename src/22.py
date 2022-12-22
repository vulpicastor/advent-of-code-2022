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
DAY = 22


MOVES = [
    np.array([ 0,  1]),
    np.array([ 1,  0]),
    np.array([ 0, -1]),
    np.array([-1,  0]),
]

FACING = ['>', 'v', '<', '^']


def do_moves(moves, walls, row_wraps, col_wraps):
    facing = 0
    pos = np.array([0, row_wraps[0].lo])
    next_pos = pos.copy()
    print(pos)
    for m in moves:
        match m:
            case int(n):
                if facing % 2 == 0:
                    wrap_func = row_wraps[pos[0]]
                else:
                    wrap_func = col_wraps[pos[1]]
                for _ in range(n):
                    next_pos += MOVES[facing]
                    if facing % 2 == 0:
                        next_pos[1] = wrap_func(next_pos[1])
                    else:
                        next_pos[0] = wrap_func(next_pos[0])
                    if tuple(next_pos) in walls:
                        break
                    pos[:] = next_pos
                next_pos[:] = pos
                print(pos, n, FACING[facing])
            case 'L':
                facing = (facing - 1) % 4
            case 'R':
                facing = (facing + 1) % 4
            case '':
                pass
            case _:
                raise ValueError('Unknown move: ', m)
        # print(pos, FACING[facing])
    return pos[0], pos[1], facing


def parse_grove(inlist):
    grid = np.zeros((len(inlist), max(map(len, inlist))), dtype=np.int8)
    for i, row in enumerate(inlist):
        for j, c in enumerate(row):
            match c:
                case '.':
                    grid[i, j] = -1
                case ' ':
                    pass
                case '#':
                    grid[i, j] = 1
                case _:
                    raise ValueError('Unexpected tile: ', c)
    return grid


def find_wrap_func(line):
    for lo, x in enumerate(line):
        if x != 0:
            break
    for hi, x in enumerate(reversed(line)):
        if x != 0:
            break
    hi = len(line) - hi
    return make_wrap_func(lo, hi)


class WrapFunc:

    def __init__(self, lo, hi):
        self.width = hi - lo
        self.lo = lo

    def __repr__(self):
        return f'WrapFunc({self.lo}, {self.lo+self.width})'

    def __call__(self, i):
        return (i - self.lo) % self.width + self.lo


@functools.cache
def make_wrap_func(lo, hi):
    return WrapFunc(lo, hi)
    # width = hi - lo
    # def wrap(i):
    #     return (i - lo) % width + lo
    # return wrap


def main():
    data = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""
    data = aocd.get_data(day=DAY, year=YEAR)
    inlist, pathing = data.split('\n\n')
    inlist = inlist.split('\n')
    grid = parse_grove(inlist)
    print(grid)
    walls = frozenset(map(tuple, np.argwhere(grid == 1)))
    print(walls)
    row_wraps = list(map(find_wrap_func, grid))
    col_wraps = list(map(find_wrap_func, grid.T))
    print(row_wraps)
    print(col_wraps)

    moves = functools.reduce(
        op.add,
        ([int(a), b] for a, b in re.findall(r'(\d+)([L|R]?)', pathing))
    )
    print(moves)

    # print(grid[tuple(np.array([0, 0]))])

    i, j, facing = do_moves(moves, walls, row_wraps, col_wraps)
    answer = 1000 * (i + 1) + 4 * (j + 1) + facing
    print(answer)
    aocd.submit(answer, part='a', day=DAY, year=YEAR)

    # answer = 
    # print(answer)
    # aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
