#!/usr/bin/env python3

# pylint: disable=unused-import
import collections
import functools
import heapq
import io
import itertools
import operator as op
import re
import timeit

import numpy as np
import aocd

import tulun

YEAR = 2022
DAY = 24


FACING = ['>', 'v', '<', '^']
INTERN_DICT = {k: k for k in FACING}
INTERN_DICT['#'] = '#'


class BlizzardValley:

    def __init__(self, inlist):
        super().__init__()
        self.grid = [[[] if c == '.' else [INTERN_DICT[c]] for c in l[1:-1]] for l in inlist[1:-1]]
        h = len(self.grid)
        w = len(self.grid[0])
        self.shape = (h, w)
        self.tmp_grid = [[[] for _ in range(w)] for _ in range(h)]
        self.cycle = np.lcm(h, w)
        self.history = np.zeros((self.cycle, h, w), dtype=int)

        move_func = [
            lambda i, j: (i, (j + 1) % w),
            lambda i, j: ((i + 1) % h, j),
            lambda i, j: (i, (j - 1) % w),
            lambda i, j: ((i - 1) % h, j),
        ]
        self.move_func = dict(zip(FACING, move_func))
        self.step = 0

        self.digraph = tulun.Digraph()
        self.start = self.digraph.add((0, -1, 0))
        self.snapshots = [[self.start]]
        self.end = self.digraph.add('end')

    def print_grid(self):
        for row in self.grid:
            print_row = []
            for cell in row:
                if not cell:
                    print_row.append('.')
                elif (cell_len := len(cell)) == 1:
                    print_row.append(cell[0])
                else:
                    print_row.append(str(cell_len))
            print(''.join(print_row))

    def bfs(self):
    # def basic_search(self, queue_class, select_func, append_func, dest=None, max_depth=None):
        """Generic implemenation of a basic graph search algorithm."""
        start = self.start
        dest = self.end
        distances = {start: 0}
        parents = {start: None}
        queue = collections.deque([start])
        found = False
        while queue:
            visit_node = queue.popleft()
            for neighbor in visit_node:
                if neighbor in distances:
                    continue
                distances[neighbor] = distances[visit_node] + 1
                parents[neighbor] = visit_node
                if neighbor is dest:
                    found = True
                    break
                queue.append(neighbor)
            if found:
                break
        return distances, parents

    def step_sim(self):
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                while cell:
                    b = cell.pop()
                    new_i, new_j = self.move_func[b](i, j)
                    self.tmp_grid[new_i][new_j].append(b)
        self.grid, self.tmp_grid = self.tmp_grid, self.grid
        self.step += 1

    def run_sim(self):
        for i in range(self.cycle):
            self.history[i] = np.array([[len(c) for c in row] for row in self.grid])
            self.step_sim()

    def _grow_graph(self):
        h, w = self.shape
        new_snapshot = []
        for node in self.snapshots[-1]:
            t, i, j = node.k
            assert t + 1 == self.step
            for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_i = i + di
                new_j = j + dj
                if self.in_bound(new_i, new_j) and not self.grid[new_i][new_j]:
                    if (new_pos := (t + 1, new_i, new_j)) not in self.digraph:
                        new_node = self.digraph.add(new_pos)
                    else:
                        new_node = self.digraph[new_pos]
                    new_snapshot.append(new_node)
                    self.digraph.adde(node, new_node)
                elif new_i == h and new_j == w - 1:
                    self.digraph.adde(node, self.end)
                    return False
        return True

    def janky_bfs(self):
        start = (0, -1, 0)
        dists = dict()
        dists[start] = 0
        parents = dict()
        parents[start] = None
        queue = collections.deque()
        queue.append(start)

        found = False
        while queue:
            visit_node = queue.popleft()
            t, i, j = visit_node
            for di, dj in [(0, 0), (0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_i = i + di
                new_j = j + dj
                neigh = (t + 1, new_i, new_j)
                # If it is actually an allowed position
                if ((i == -1 and j == 0 and new_i == -1 and j == 0)
                    or (self.in_bound(new_i, new_j)
                        and self.history[(t + 1) % self.cycle, new_i, new_j] == 0)):
                    dists[neigh] = dists[visit_node] + 1
                    parents[neigh] = visit_node
                    queue.append(neigh)
                # Except if it's actually the desired end point
                if new_i == self.shape[0] and new_j == self.shape[1] - 1:
                    dists['end'] = dists[visit_node] + 1
                    parents['end'] = visit_node
                    found = True
                    break
            if found:
                break
        return dists, parents

    def astar(self):
        h, w = self.shape
        def heuristic(node):
            _, i, j = node
            return abs(h - i) + abs(w - 1 - j)
        start = (0, -1, 0)
        dists = dict()
        dists[start] = 0
        parents = dict()
        parents[start] = None
        queue = []
        heapq.heappush(queue, (0, start))

        found = False
        while queue:
            _, visit_node = heapq.heappop(queue)
            print(_, visit_node)
            t, i, j = visit_node
            for di, dj in [(0, 0), (0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_i = i + di
                new_j = j + dj
                # If it's actually the desired end point
                if new_i == self.shape[0] and new_j == self.shape[1] - 1:
                    dists['end'] = dists[visit_node] + 1
                    parents['end'] = visit_node
                    found = True
                    break
                neigh = (t + 1, new_i, new_j)
                if neigh in dists:
                    continue
                # If it is actually an allowed position
                if ((i == -1 and j == 0 and new_i == -1 and j == 0)
                    or (self.in_bound(new_i, new_j)
                        and self.history[(t + 1) % self.cycle, new_i, new_j] == 0)):
                    dists[neigh] = dists[visit_node] + 1
                    parents[neigh] = visit_node
                    heapq.heappush(queue, (dists[neigh] + heuristic(neigh), neigh))
            if found:
                break
        return dists, parents

    def in_bound(self, i, j):
        h, w = self.shape
        if 0 <= i < h and 0 <= j < w:
            return True
        return False


def make_grid(inlist, grid):
    pass


def main():
    data = """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#"""
    data = aocd.get_data(day=DAY, year=YEAR)
    inlist = data.split('\n')
    # sim = BlizzardValley(inlist)
    # for i in range(19):
    #     print(i)
    #     sim.print_grid()
    #     sim.step_sim()
    sim = BlizzardValley(inlist)
    sim.run_sim()
    # print(sim.history)

    dists, parents = sim.astar()
    # print(dists, parents)
    print(dists)
    print(parents)
    path = ['end']
    backtrack = 'end'
    while parents[backtrack] is not None:
        backtrack = parents[backtrack]
        path.append(backtrack)
    print(list(reversed(path)))
    print(dists['end'])

    # answer = 
    # print(answer)
    # aocd.submit(answer, part='a', day=DAY, year=YEAR)

    # answer = 
    # print(answer)
    # aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
