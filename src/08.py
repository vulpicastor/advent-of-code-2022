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
        # print(scores)
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
    # aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
