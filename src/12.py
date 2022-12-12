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

import tulun

YEAR = 2022
DAY = 12

ORD_S = ord('S')
ORD_E = ord('E')


def height(s):
    if s == ORD_S:
        return ord('a')
    if s == ORD_E:
        return ord('z')
    return s


def parse_map(grid):
    n_row, n_col = grid.shape
    my_grid = np.zeros((n_row+2, n_col+2), dtype=np.int8)
    my_grid[1:-1, 1:-1] = grid
    checked = set()
    for border in itertools.product([0, n_row+1], range(n_col+2)):
        checked.add(border)
    for border in itertools.product(range(n_row+2), [0, n_col+1]):
        checked.add(border)
    # print(checked)
    edges = []
    start = None
    end = None
    for my_pos in itertools.product(range(1, n_row+1), range(1, n_col+1)):
        # print(my_pos)
        i, j = my_pos
        if my_grid[my_pos] == ORD_S:
            start = my_pos
        elif my_grid[my_pos] == ORD_E:
            end = my_pos
        my_h = height(my_grid[my_pos])
        for di, dj in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            neigh_pos = (i + di, j + dj)
            if neigh_pos in checked:
                continue
            neigh_h = height(my_grid[neigh_pos])
            diff_h = neigh_h - my_h
            if diff_h > 1:
                continue
            edges.append((my_pos, neigh_pos, 1))
            if diff_h < -1:
                continue
            edges.append((neigh_pos, my_pos, 1))
        checked.add(my_pos)
    graph = tulun.Digraph(edges)
    return graph, graph[start], graph[end]


def parse_map2(grid):
    n_row, n_col = grid.shape
    my_grid = np.zeros((n_row+2, n_col+2), dtype=np.int8)
    my_grid[1:-1, 1:-1] = grid
    checked = set()
    for border in itertools.product([0, n_row+1], range(n_col+2)):
        checked.add(border)
    for border in itertools.product(range(n_row+2), [0, n_col+1]):
        checked.add(border)
    # print(checked)
    edges = []
    starts = []
    end = None
    for my_pos in itertools.product(range(1, n_row+1), range(1, n_col+1)):
        # print(my_pos)
        i, j = my_pos
        if my_grid[my_pos] == ORD_S:
            starts.append(my_pos)
        elif my_grid[my_pos] == ORD_E:
            end = my_pos
        my_h = height(my_grid[my_pos])
        if my_h == ord('a'):
            starts.append(my_pos)
        for di, dj in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            neigh_pos = (i + di, j + dj)
            if neigh_pos in checked:
                continue
            neigh_h = height(my_grid[neigh_pos])
            diff_h = my_h - neigh_h
            if diff_h <= 1:
                edges.append((my_pos, neigh_pos, 1))
            if diff_h >= -1:
                edges.append((neigh_pos, my_pos, 1))
        checked.add(my_pos)
    graph = tulun.Digraph(edges)
    return graph, [graph[n] for n in starts], graph[end]


def main():
    data = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""
    data = aocd.get_data(day=DAY, year=YEAR)
    inlist = np.array([[ord(c) for c in l] for l in data.split('\n')], dtype=np.int8)
    # print(inlist)

    my_graph, start, end = parse_map(inlist)
    # print(my_graph)

    distances, parents = start.bfs(end)
    # print(distances)
    # print(parents)
    answer = distances[end]
    print(answer)
    # aocd.submit(answer, part='a', day=DAY, year=YEAR)

    re_graph, starts, end = parse_map2(inlist)
    distances, _ = end.bfs()
    # print(distances)
    answer = min(distances[n] for n in starts if n in distances)
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
