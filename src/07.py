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
DAY = 7


class MyDir(collections.UserDict):

    def __init__(self, fn, parent=None):
        super().__init__()
        self.fn = fn
        if parent is None:
            self.parent = self
        else:
            self.parent = parent

    def add_file(self, fn, size):
        self.data[fn] = size

    def add_dir(self, fn):
        if not fn in self.data:
            self.data[fn] = MyDir(fn, self)

    def du(self):
        size = 0
        for _, v in self.items():
            if isinstance(v, MyDir):
                size += v.du()
            else:
                size += v
        return size

    def du_r(self):
        sizes = []
        my_size = 0
        for _, v in self.items():
            if isinstance(v, MyDir):
                c_sizes = v.du_r()
                my_size += c_sizes[-1]
                sizes.extend(c_sizes)
            else:
                my_size += v
        sizes.append(my_size)
        return sizes


def parse_tree(lines, root=None):
    if root is None:
        root = MyDir('/')
    state = root
    for l in lines:
        match l.split():
            case ['$', 'cd', '/']:
                state = root
            case ['$', 'cd', '..']:
                state = state.parent
            case ['$', 'cd', fn]:
                if fn in state:
                    state = state[fn]
                else:
                    state.add_dir(fn)
                    state = state[fn]
            case ['$', 'ls']:
                continue
            case ['dir', fn]:
                state.add_dir(fn)
            case [size, fn]:
                state.add_file(fn, int(size))
    return root


def main():
    data = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""
    data = aocd.get_data(day=DAY, year=YEAR)
    inlist = [l for l in data.split('\n')]

    root = parse_tree(inlist)
    # print(root)
    du_r = root.du_r()
    answer = sum(s for s in du_r if s <= 100000)
    print(answer)
    aocd.submit(answer, part='a', day=DAY, year=YEAR)

    total_size = du_r[-1]
    free_at_least = 30000000 - (70000000 - total_size)
    answer = min(s for s in du_r if s >= free_at_least)
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
