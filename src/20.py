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
DAY = 20



class ListNode:

    def __init__(self, value=None, prev=None, succ=None):
        self.v = value
        self.p = prev
        self.n = succ

    def __iter__(self):
        node = self.n
        while node is not None:
            yield node
            node = node.n

    def move(self, x):
        if x == 0:
            return
        p = self.p
        n = self.n
        p.n, n.p = n, p
        if x > 0:
            insert_after = self
            for _ in range(x):
                insert_after = insert_after.n
        else:
            insert_after = self.p
            for _ in range(-x):
                insert_after = insert_after.p
        insert_before = insert_after.n
        insert_after.n, self.p = self, insert_after
        self.n, insert_before.p = insert_before, self



class RingBuffer:

    def __init__(self, iterable):
        super().__init__()
        iter_iter = iter(iterable)
        try:
            self.head = ListNode(next(iter_iter))
        except StopIteration:
            self.head = None
            self.orig = []
            return
        prev = self.head
        node = self.head
        self.orig = [self.head]
        for i in iter_iter:
            node = ListNode(i, prev)
            prev.n = node
            prev = node
            self.orig.append(node)
        self.head.p = node
        node.n = self.head

    def __iter__(self):
        node = self.head
        if node is None:
            return
        yield node.v
        while node.n is not self.head:
            node = node.n
            yield node.v

    def find(self, value):
        for i in self.orig:
            if i.v == value:
                return i

    def mix(self):
        modulus = len(self.orig) - 1
        offset = modulus // 2
        for i in self.orig:
            m = i.v + offset
            m %= modulus
            m -= offset
            i.move(m)



def main():
    data = """1
2
-3
3
-2
0
4"""
    data = aocd.get_data(day=DAY, year=YEAR)
    inlist = [int(l) for l in data.split('\n') if l]

    buffer = RingBuffer(inlist)
    # print(list(buffer))
    buffer.mix()
    # print(list(buffer))
    if (zero_node := buffer.find(0)) is None:
        return
    from_zero = iter(zero_node)
    answer = 0
    for _ in range(3):
        for _, i in zip(range(1000), from_zero):
            pass
        print(i.v)
        answer += i.v
    print(answer)
    aocd.submit(answer, part='a', day=DAY, year=YEAR)

    buffer = RingBuffer(l * 811589153 for l in inlist)
    # print(list(buffer))
    for _ in range(10):
        buffer.mix()
    # print(list(buffer))
    if (zero_node := buffer.find(0)) is None:
        return
    from_zero = iter(zero_node)
    answer = 0
    for _ in range(3):
        for _, i in zip(range(1000), from_zero):
            pass
        print(i.v)
        answer += i.v
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
