#!/usr/bin/env python3

# pylint: disable=unused-import
import collections
import dataclasses
import functools
import io
import itertools
import operator as op
import re
import timeit

import numpy as np
import aocd

YEAR = 2022
DAY = 23


class Grid:

    def __init__(self, inlist):
        self.locs = np.argwhere(np.array(inlist)[::-1].T == '#')
        self.buffer = np.copy(self.locs)
        self.length = len(self.locs)
        self.moves = collections.deque([
            (np.array([ 0,  1]), np.array([[-1,  1], [0,  1], [1,  1]])),
            (np.array([ 0, -1]), np.array([[-1, -1], [0, -1], [1, -1]])),
            (np.array([-1,  0]), np.array([[-1, -1], [-1, 0], [-1, 1]])),
            (np.array([ 1,  0]), np.array([[ 1, -1], [ 1, 0], [ 1, 1]])),
        ])
        self.around = np.array([
            [-1, -1],
            [-1,  0],
            [-1,  1],
            [ 0, -1],
            [ 0,  1],
            [ 1, -1],
            [ 1,  0],
            [ 1,  1],
        ])

    def __str__(self):
        lo = np.min(self.locs, axis=0)
        hi = np.max(self.locs, axis=0)
        grid = np.zeros(hi - lo + 1, dtype=bool)
        grid[tuple((self.locs - np.atleast_2d(lo)).T)] = True
        grid = grid.T[::-1]
        rows = [f"{''.join(row)} {hi[1] - i}"
                for i, row in enumerate(np.where(grid, '#', '.'))]
        rows.append(str(lo[0]))
        return '\n'.join(rows)
        # return '\n'.join(''.join(
                # '#' if c else '.' for c in row) +  for i, row in enumerate(grid))

    def propose(self):
        pos_set = set(list(map(tuple, self.locs)))
        for i, pos in enumerate(self.locs):
            if all(tuple(new_pos) not in pos_set for new_pos in pos + self.around):
                # self.buffer[i] = pos
                continue
            for mvmt, check_delta in self.moves:
                if all(tuple(new_pos) not in pos_set for new_pos in pos + check_delta):
                    self.buffer[i] = pos + mvmt
                    break
            # else:
                # self.buffer[i] = pos
        self.moves.rotate(-1)

    def update_locs(self):
        pos_count = collections.Counter(map(tuple, self.buffer))
        # self.locs = np.where(
        #     [pos_count[tuple(pos)] == 1 for pos in self.buffer],
        #     self.locs, self.buffer,
        # )
        for i, pos in enumerate(self.buffer):
            if pos_count[tuple(pos)] > 1:
                continue
            self.locs[i] = pos
        self.buffer[:] = self.locs



def main():
    data = """.....
..##.
..#..
.....
..##.
....."""
    data = """....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#.."""
    data = aocd.get_data(day=DAY, year=YEAR)
    inlist = [list(l) for l in data.split('\n')]
    grid = Grid(inlist)
    print(grid)
    # print(grid.locs)
    for _ in range(10):
        grid.propose()
        print(grid.buffer)
        grid.update_locs()
        print(grid)
    lo = np.min(grid.locs, axis=0)
    hi = np.max(grid.locs, axis=0)
    answer = np.product(hi - lo + 1) - grid.length
    print(answer)
    # aocd.submit(answer, part='a', day=DAY, year=YEAR)

    grid = Grid(inlist)
    for i in range(1000):
        grid.propose()
        if np.all(grid.buffer == grid.locs):
            break
        grid.update_locs()
    print(grid)
    answer = i + 1
    print(answer)
    # aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
