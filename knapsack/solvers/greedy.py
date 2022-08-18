from operator import attrgetter
from random import shuffle
from solvers.utils import parser_input, parser_output

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
    
    output_data = parser_output(value, taken)
    return output_data

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
    
    output_data = parser_output(value, taken)
    return output_data

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
    
    output_data = parser_output(value, taken)
    return output_data

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
    output_data = parser_output(value, taken)
    return output_data