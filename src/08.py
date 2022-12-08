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
DAY = 8



def visible(grid):
    n_row, n_col = grid.shape
    from_left = np.zeros_like(grid, dtype=bool)
    for i, row in enumerate(grid):
        tallest = -1
        for j, h in enumerate(row):
            if h > tallest:
                from_left[i, j] = True
                tallest = h
    from_right = np.zeros_like(grid, dtype=bool)
    for i, row in enumerate(grid):
        tallest = -1
        for j, h in enumerate(reversed(row)):
            if h > tallest:
                from_right[i, n_col-j-1] = True
                tallest = h
    from_top = np.zeros_like(grid, dtype=bool)
    for j, col in enumerate(grid.T):
        tallest = -1
        for i, h in enumerate(col):
            if h > tallest:
                from_top[i, j] = True
                tallest = h
    from_bottom = np.zeros_like(grid, dtype=bool)
    for j, col in enumerate(grid.T):
        tallest = -1
        for i, h in enumerate(reversed(col)):
            if h > tallest:
                from_bottom[n_row-i-1, j] = True
                tallest = h
    return from_left | from_right | from_top | from_bottom

def viewing(grid):
    n_row, n_col = grid.shape
    grid_score = np.zeros_like(grid)
    for i, j in itertools.product(range(1, n_row-1), range(1, n_col-1)):
        shorter = grid < grid[i, j]
        scores = []
        for n, vi in enumerate(range(i-1, -1, -1)):
            if not shorter[vi, j]:
                scores.append(n + 1)
                break
        else:
            scores.append(i)
        for n, vi in enumerate(range(i+1, n_row)):
            if not shorter[vi, j]:
                scores.append(n + 1)
                break
        else:
            scores.append(n_row - i - 1)
        for n, vj in enumerate(range(j-1, -1, -1)):
            if not shorter[i, vj]:
                scores.append(n + 1)
                break
        else:
            scores.append(j)
        for n, vj in enumerate(range(j+1, n_col)):
            if not shorter[i, vj]:
                scores.append(n + 1)
                break
        else:
            scores.append(n_col - j - 1)
        print(scores)
        grid_score[i, j] = functools.reduce(op.mul, scores)
    return grid_score



def main():
    data = """30373
25512
65332
33549
35390"""
    data = aocd.get_data(day=DAY, year=YEAR)
    inlist = [list(map(int, l)) for l in data.split('\n')]
    grid = np.array(inlist)
    print(grid)

    answer = np.sum(visible(grid))
    print(answer)
    # aocd.submit(answer, part='a', day=DAY, year=YEAR)

    answer = np.max(viewing(grid))
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
