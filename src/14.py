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
DAY = 14



def make_grid(paths):
    min_x = min(min(i[0] for i in p) for p in paths)
    max_x = max(max(i[0] for i in p) for p in paths)
    max_y = max(max(i[1] for i in p) for p in paths)
    print(min_x, max_x)
    min_x -= 1
    grid = np.zeros((max_y + 3, max_x - min_x + 2))
    for p in paths:
        for (x0, y0), (x1, y1) in itertools.pairwise(p):
            startx = min(x0, x1) - min_x
            endx = max(x0, x1) - min_x + 1
            starty = min(y0, y1)
            endy = max(y0, y1) + 1
            grid[starty:endy, startx:endx] = 1
    return grid, min_x


def add_sand(grid, start_col):
    n_row, n_col = grid.shape
    j = start_col
    for i in range(n_row-1):
        # print(i, j)
        if j < 0 or j >= n_col:
            return None
        if grid[i + 1, j] == 0:
            continue
        if grid[i + 1, j - 1] == 0:
            j -= 1
            continue
        if grid[i + 1, j + 1] == 0:
            j += 1
            continue
        return i, j
    return None

def add_sand2(grid, start_col):
    n_row, n_col = grid.shape
    j = start_col
    for i in range(n_row-1):
        # print(i, j)
        # if j < 0 or j >= n_col:
            # return n_row - i - 1, (i - 1)
        if grid[i + 1, j] == 0:
            continue
        if j == 0:
            return n_row - i - 1, (i, j)
        if grid[i + 1, j - 1] == 0:
            j -= 1
            continue
        if j == n_col - 1:
            return n_row - i - 1, (i, j)
        if grid[i + 1, j + 1] == 0:
            j += 1
            continue
        return 1, (i, j)
    return None


def fill_sand(grid, min_x):
    start_col = 500 - min_x
    n_sand = 0
    # for _ in range(2):
    while (pos := add_sand(grid, start_col)) is not None:
        # pos = add_sand(grid, start_col)
        # if pos is None:
            # break
        print(pos)
        n_sand += 1
        grid[pos] = -1
        # print_grid(grid)
    return n_sand


def fill_sand2(grid, min_x):
    start_col = 500 - min_x
    n_sand = 0
    # for _ in range(2):
    while (res := add_sand2(grid, start_col)) is not None:
        new_sand, pos = res
        print(new_sand, pos)
        n_sand += new_sand
        grid[pos] = -1
        # print_grid(grid)
        if pos[0] == 0:
            n_sand += 1
            break
    return n_sand


def sum_first(n):
    if n % 2:
        return (1 + n) // 2 * n
    return n // 2 * (1 + n)



def print_grid(grid):
    for row in grid:
        print_row = []
        for col in row:
            match col:
                case 0:
                    print_row.append('.')
                case 1:
                    print_row.append('#')
                case -1:
                    print_row.append('o')
        print(''.join(print_row))


def main():
    data = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""
    data = aocd.get_data(day=DAY, year=YEAR)
    inlist = [
        [[int(i) for i in n.split(',')] for n in l.split(' -> ')]
        for l in data.split('\n')
    ]
    grid, min_x = make_grid(inlist)
    print_grid(grid)

    answer = fill_sand(grid, min_x)
    print_grid(grid)
    print(answer)
    # aocd.submit(answer, part='a', day=DAY, year=YEAR)

    grid, min_x = make_grid(inlist)
    grid[-1] = 1
    answer = fill_sand2(grid, min_x)
    print_grid(grid)
    print(answer)
    sand_in_grid = np.count_nonzero(grid == -1)
    left_sand_i = np.argmin(grid[:, 0])
    right_sand_i = np.argmin(grid[:, -1])
    n_row = grid.shape[0]
    print(sand_in_grid +
        sum_first(n_row - left_sand_i - 2) +
        sum_first(n_row - right_sand_i - 2) + 1)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
