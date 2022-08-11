from operator import attrgetter
from random import shuffle
from utils import parser_input, parser_output

def priority_value(input_data):
    """ Greedly insert items in knapsack based on value 

    Args:
        input_data (str): The data of knapsack instance
    
    Returns:
        output_data (str): Specific format to submit assignment to Coursera
    """
    item_count, capacity, items = parser_input(input_data)
    value = 0
    weight = 0
    taken = [0] * item_count

    for item in sorted(items, key=attrgetter('value'), reverse=True):
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight
    
    return parser_output(value, taken)

def priority_weight(input_data):
    """ Greedly insert items in knapsack based on weight 

    Args:
        input_data (str): The data of knapsack instance
    
    Returns:
        output_data (str): Specific format to submit assignment to Coursera
    """
    item_count, capacity, items = parser_input(input_data)
    value = 0
    weight = 0
    taken = [0] * item_count

    for item in sorted(items, key=attrgetter('weight'), reverse=True):
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight
    
    return parser_output(value, taken)

def priority_density(input_data):
    """ Greedly insert items in knapsack based on density (value / weight)

    Args:
        input_data (str): The data of knapsack instance
    
    Returns:
        output_data (str): Specific format to submit assignment to Coursera
    """
    item_count, capacity, items = parser_input(input_data)
    value = 0
    weight = 0
    taken = [0] * item_count

    for item in sorted(items, key=attrgetter('density'), reverse=True):
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight
    
    return parser_output(value, taken)

def random_solution(input_data):
    """ Randomly insert items in knapsack

    Args:
        input_data (str): The data of knapsack instance
    
    Returns:
        output_data (str): Specific format to submit assignment to Coursera
    """
    item_count, capacity, items = parser_input(input_data)
    value = 0
    weight = 0
    taken = [0] * item_count
    shuffle(items)
    for item in items:
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight
    return parser_output(value, taken)

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(priority_value(input_data))
        print(priority_weight(input_data))
        print(priority_density(input_data))
        print(random_solution(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')