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
from typing import Callable, Optional

import numpy as np
import aocd

YEAR = 2022
DAY = 21


MAP_OP = {
    '+': op.add,
    '-': op.sub,
    '*': op.mul,
    '/': op.floordiv,
}
OP_STR = {v: k for k, v in MAP_OP.items()}

@dataclasses.dataclass(unsafe_hash=True)
class Expr:
    name: Optional[str] = None
    func: Optional[Callable] = None
    children: Optional[tuple["Expr", "Expr"]] = None
    value: Optional[int | float] = None

    def __str__(self):
        if self.name == 'humn':
            return 'humn'
        if self.value is not None:
            return str(self.value)
        if self.func is not None and self.children is not None:
            return f'({self.children[0]} {OP_STR[self.func]} {self.children[1]})'
        return f'Expr({self.name}, {self.func}, {self.children}, {self.value})'

    @functools.cache
    def eval(self):
        if self.value is not None:
            return self.value
        if self.func is not None and self.children is not None:
            return self.func(self.children[0].eval(), self.children[1].eval())
        raise ValueError('Cannot evaluate expression')


def make_symbol_table():
    return collections.defaultdict(Expr)


def parse_line(line: str, symbol_table: collections.defaultdict[str, Expr]) -> None:
    lhs, rhs = line.split(': ')
    node = symbol_table[lhs]
    node.name = lhs
    if rhs.isnumeric():
        node.value = int(rhs)
        return
    token1, op_token, token2 = rhs.split()
    node.func = MAP_OP[op_token]
    node.children = symbol_table[token1], symbol_table[token2]


def main():
    data = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""
    data = aocd.get_data(day=DAY, year=YEAR)
    inlist = [l for l in data.split('\n')]

    symbols = make_symbol_table()
    for l in inlist:
        parse_line(l, symbols)
    answer = symbols['root'].eval()
    print(answer)
    aocd.submit(answer, part='a', day=DAY, year=YEAR)

    symbols = make_symbol_table()
    for l in inlist:
        parse_line(l, symbols)
    print(symbols['root'].children[0])
    print()
    print(symbols['root'].children[1])
    # print(answer)
    # aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
