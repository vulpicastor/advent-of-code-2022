#!/usr/bin/env python3

import itertools
import functools
import operator as op

import numpy as np
import aocd

YEAR = 2022
DAY = 8


def _visible(grid):
    n_row = len(grid)
    viz = np.zeros_like(grid, dtype=bool)
    # From top edge.
    tallest = grid[0].copy()
    for i in range(1, n_row-1):
        row = grid[i]
        viz[i] |= row > tallest
        np.maximum(tallest, row, out=tallest)
    tallest[:] = grid[-1]
    # From bottom edge.
    for i in reversed(range(1, n_row-1)):
        row = grid[i]
        viz[i] |= row > tallest
        np.maximum(tallest, row, out=tallest)
    return viz


def visible(grid):
    # Left and right edges are the top and bottom edges of the transpose.
    viz = _visible(grid) | (_visible(grid.T)).T
    # Set all edge trees to visible.
    viz[[0, -1]] = True
    viz[:, [0, -1]] = True
    return viz


def viewing(grid):
    n_row, n_col = grid.shape
    grid_score = np.zeros_like(grid)
    for i, j in itertools.product(range(1, n_row-1), range(1, n_col-1)):
        shorter_row = grid[i] < grid[i, j]
        shorter_col = grid[:, j] < grid[i, j]
        scores = []
        # np.argmin conveniently returns the index of the first minimum value.
        # But if the slice is all True, then it would always return index 0,
        # in which case the correct value is the length of the slice.
        to_top = shorter_col[:i][::-1]
        scores.append(i if np.all(to_top) else (np.argmin(to_top) + 1))
        to_left = shorter_row[:j][::-1]
        scores.append(j if np.all(to_left) else (np.argmin(to_left) + 1))
        to_bottom = shorter_col[i+1:]
        scores.append(n_row - i - 1 if np.all(to_bottom) else (np.argmin(to_bottom) + 1))
        to_right = shorter_row[j+1:]
        scores.append(n_col - j - 1 if np.all(to_right) else (np.argmin(to_right) + 1))
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
    aocd.submit(answer, part='a', day=DAY, year=YEAR)

    answer = np.max(viewing(grid))
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
