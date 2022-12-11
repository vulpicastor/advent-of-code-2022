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
DAY = 11


class Monkey:

    def __init__(self, rules):
        self.items = collections.deque(
            int(n.strip()) for n in (rules[1].split(':'))[1].split(', '))
        op_tokens = rules[2].split()
        operator = {'*': op.mul, '+': op.add}[op_tokens[4]]
        if op_tokens[5] == 'old':
            self.operate = lambda x: operator(x, x)
        else:
            operand = int(op_tokens[5])
            self.operate = lambda x: operator(x, operand)
        self.dividend = int((rules[3].split())[3])
        self.if_true = int(rules[4][-1])
        self.if_false = int(rules[5][-1])
        self.handled = 0

    def append(self, x):
        self.items.append(x)

    def extend(self, x):
        self.items.extend(x)

    def dispatch(self, global_div=None):
        self.handled += len(self.items)
        inspects = np.array(self.items)
        inspects = self.operate(inspects)
        if global_div is None:
            inspects //= 3
        else:
            inspects %= global_div
        self.items.clear()
        dispatcher = [[] for _ in range(8)]
        for w, m in zip(inspects, np.mod(inspects, self.dividend)==0):
            dispatcher[self.if_true if m else self.if_false].append(w)
        return dispatcher

def do_round(monkeys):
    for m in monkeys:
        to_dispatch = m.dispatch()
        # print(to_dispatch)
        for new_m, worries in zip(monkeys, to_dispatch):
            new_m.extend(worries)

def do_round2(monkeys, global_div):
    for m in monkeys:
        to_dispatch = m.dispatch(global_div)
        # print(to_dispatch)
        for new_m, worries in zip(monkeys, to_dispatch):
            new_m.extend(worries)

def main():
    data = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""
    data = aocd.get_data(day=DAY, year=YEAR)
    inlist = [l.split('\n') for l in data.split('\n\n')]

    monkeys = list(map(Monkey, inlist))
    old_num_items = sum(len(m.items) for m in monkeys)
    # print([[m.items, m.dividend, m.if_true, m.if_false] for m in monkeys])
    for _ in range(20):
        do_round(monkeys)
        # print([m.items for m in monkeys])
    handling = [m.handled for m in monkeys]
    handling.sort()
    # print([m.dispatch() for m in monkeys])
    answer = handling[-1] * handling[-2]
    new_num_items = sum(len(m.items) for m in monkeys)
    print(old_num_items, new_num_items)
    print(answer)
    # aocd.submit(answer, part='a', day=DAY, year=YEAR)

    monkeys = list(map(Monkey, inlist))
    global_div = functools.reduce(op.mul, (m.dividend for m in monkeys))
    for _ in range(10000):
        do_round2(monkeys, global_div)
        # print([m.items for m in monkeys])
    handling = [m.handled for m in monkeys]
    handling.sort()
    answer = handling[-1] * handling[-2]
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
