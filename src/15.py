#!/usr/bin/env python3

# pylint: disable=unused-import
import collections
import functools
import io
import itertools
import operator as op
import re
import timeit
import tqdm

import numpy as np
import aocd

YEAR = 2022
DAY = 15


def parse_line(l):
    m = re.match(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)', l)
    if m is None:
        return None
    return np.array([int(m.group(1)), int(m.group(2))]), np.array([int(m.group(3)), int(m.group(4))])


def metric(a, b):
    return np.sum(np.abs(a - b))


def exclude_x_range_at_y(y, pos_pair, exclude_known=True):
    sensor, beacon = pos_pair
    dist = metric(sensor, beacon)
    if y < sensor[1] - dist or sensor[1] + dist < y:
        return None
    exclude_x_dist = dist - abs(sensor[1] - y)
    start = sensor[0] - exclude_x_dist
    end = sensor[0] + exclude_x_dist + 1
    if not exclude_known:
        return start, end
    if y != beacon[1]:
        return start, end
    if beacon[0] == start:
        start += 1
    elif beacon[0] == end - 1:
        end -= 1
    return start, end


def combine(ranges):
    new_list = list(set(itertools.chain(*itertools.starmap(range, ranges))))
    new_list.sort()
    return new_list

def count_ranges(ranges):
    return len(set(itertools.chain(*itertools.starmap(range, ranges))))

def search(y, pos_pairs, buffer):
    x_lim = len(buffer)
    buffer[:] = True
    for p in pos_pairs:
        if (range_arg := exclude_x_range_at_y(y, p)) is None:
            continue
        start, end = range_arg
        start = max(0, start)
        end = min(x_lim, end)
        buffer[start:end] = False
        beacon = p[1]
        if beacon[1] == y:
            buffer[beacon[0]] = False
    # print(buffer)
    if np.any(buffer):
        return np.argmax(buffer)
    return None


def merge_ranges(ranges):
    my_ranges = list(filter(lambda x: x is not None and x[0] != x[1], ranges))
    my_ranges.sort()
    stack = [my_ranges[0]]
    for r in my_ranges[1:]:
        old_start, old_end = stack[-1]
        if old_end >= r[0]:
            new_end = max(old_end, r[1])
            stack.pop()
            stack.append((old_start, new_end))
        else:
            stack.append(r)
    return stack


def main():
    data = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""
    data = aocd.get_data(day=DAY, year=YEAR)
    inlist = list(filter(None, (parse_line(l) for l in data.split('\n'))))
    # print(inlist)

    exclude_dist = list(itertools.starmap(metric, inlist))
    # print(exclude_dist)
    # for row in range(12):
    #     print(row, list(exclude_x_range_at_y(row, p, d) for p, d in zip(inlist, exclude_dist)))
    #     print(row, combine(filter(None,
    #         (exclude_x_range_at_y(row, p, d) for p, d in zip(inlist, exclude_dist)))))
    answer = count_ranges(
        filter(
            None,
            (
                exclude_x_range_at_y(2000000, p)
                for p, d in zip(inlist, exclude_dist)
            )
        )
    )
    print(answer)
    # aocd.submit(answer, part='a', day=DAY, year=YEAR)

    xy_max = 20
    xy_max = 4000000
    # buffer = np.ones(xy_max + 1, dtype=bool)
    for y in tqdm.tqdm(range(xy_max + 1), miniters=100000):
        merged_r = merge_ranges(exclude_x_range_at_y(y, p, exclude_known=False) for p in inlist)
        if len(merged_r) > 1:
            print(y, merged_r)
            break
        # if (res := search(y, inlist, buffer)) is not None:
            # print(res)
            # x = res
            # break
    else:
        raise ValueError()
    # answer = x * 4000000 + y
    # print(answer)
    # aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
