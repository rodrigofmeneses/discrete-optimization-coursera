#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from collections import namedtuple
from solvers.two_opt import two_opt
from solvers.greedy import nearest_neighbor

Point = namedtuple("Point", ['x', 'y'])

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def solve_it(input_data):
    match int(input_data.split()[0]):
        case 1889 | 33810:
            return nearest_neighbor(input_data)
        case _:
            return two_opt(input_data)


import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')

