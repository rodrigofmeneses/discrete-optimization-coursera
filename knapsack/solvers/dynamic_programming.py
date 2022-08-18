import sys
from solvers.utils import parser_input, parser_output

def fill_optimal_table(capacity, items):
    """ Fill the optimal table to avoid recursion.
        optimal_table[capacity][index] means the optimal value for this capacity
        with number items equal index number evalueted.

    Args:
        capacity (int): The capacity of knapsack
        items (list[Item]): List of items to choose
    
    Returns:
        optimal_table (list[list[int]]): 2D array with the optimal value
            for each weight of knapsack
    """
    # Create a 2D array of shape (number_of_items x capacity_of_knapsack) with 0 values.
    optimal_table = [
        [0 for _ in range(len(items))] for _ in range(capacity + 1)
    ]

    # Logic of Dynamic Programming.
    for item in items:
        for k in range(1, capacity + 1):
            if item.weight <= k:
                optimal_table[k][item.index] = max(
                    optimal_table[k][item.index - 1],
                    item.value + optimal_table[k - item.weight][item.index - 1]
                )
            else:
                optimal_table[k][item.index] = optimal_table[k][item.index - 1]
    return optimal_table

def trace(optimal_table, items):
    """ Trace the items taken from a optimal table.

    Args:
        optimal_table (list[list[int]]): 2D array with the optimal value
            for each weight of knapsack
        items (list[Item]): List of items to choose
    
    Returns:
        taken (list[int]): List of items taken, a solution of problem
    """
    num_items = len(items)
    capacity = len(optimal_table) - 1
    taken = [0] * num_items
    
    for index in range(num_items - 1, 0, -1):
        if optimal_table[capacity][index] != optimal_table[capacity][index - 1]:
            taken[index] = 1
            capacity -= items[index].weight
    return taken

def dynamic_programming(input_data):
    """ Dynamic Programming aprouch to solve knapsack problem

    Args:
        input_data (str): The data of knapsack instance
    
    Returns:
        output_data (str): Specific format to submit assignment to Coursera
    """
    item_count, capacity, items = parser_input(input_data)
    optimal_table = fill_optimal_table(capacity, items)
    value = optimal_table[capacity][item_count - 1]
    taken = trace(optimal_table, items)

    output_data = parser_output(value, taken, optimal=1)
    return output_data