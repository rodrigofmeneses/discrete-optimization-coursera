#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
from solvers.greedy import priority_density, priority_value, priority_weight
from solvers.dynamic_programming import dynamic_programming
from solvers.branch_and_bound import BranchAndBound
Item = namedtuple("Item", ['index', 'value', 'weight'])

def greedy(input_data):
    greedy_density = priority_density(input_data)
    greedy_value = priority_value(input_data)
    greedy_weight = priority_weight(input_data)
    
    density_objective = float(greedy_density.split()[0])
    value_objective = float(greedy_value.split()[0])
    weight_objective = float(greedy_weight.split()[0])

    best_greedy = ''
    best_greedy_value = 0

    if density_objective > best_greedy_value:
        best_greedy_value = density_objective
        best_greedy = greedy_density
    if value_objective > best_greedy_value:
        best_greedy_value = value_objective
        best_greedy = greedy_value
    if weight_objective > best_greedy_value:
        best_greedy_value = weight_objective
        best_greedy = greedy_weight

    return best_greedy

def dp(input_data):
    dp = dynamic_programming(input_data)
    return dp

def bnb(input_data):
    bnb = BranchAndBound(input_data)
    return bnb.DFS()


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    match int(input_data.split()[0]):
        case 200:
            return dp(input_data)
        case 10000:
            return greedy(input_data)
        case _:
            return bnb(input_data)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

