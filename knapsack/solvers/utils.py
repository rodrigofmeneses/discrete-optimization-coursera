from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight', 'density'])

def parser_input(input_data):
    """Parser a str input to correct type to work
    
    Args:
        input_data (str): The data of knapsack instance
    
    Returns:
        item_count (int): Number of items
        capacity (int): Capacity of knapsack
        items (List(Item)): List of items with respectives values and weights
    """
    # parse the input
    lines = input_data.split('\n')
    item_count, capacity = map(int, lines[0].split())

    items = []

    for i in range(1, item_count + 1):
        line = lines[i]
        value, weight = map(int, line.split())
        items.append(Item(i - 1, value, weight, value / weight))
    
    return item_count, capacity, items

def parser_output(value, taken, optimal=0):
    """Parser objetive value and decisions variables to specific format to submit assignment to Coursera

    Args:
        value (int): Value of objective function.
        taken (list): List of boolean decision variables.
        optimal (int): Value 1 if solution is proved optimal. Default is 0.
    
    Returns:
        output_data (str): Specific format to Coursera submission
    """
    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(optimal) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data