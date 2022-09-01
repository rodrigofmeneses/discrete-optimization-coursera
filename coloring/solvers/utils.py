import networkx as nx

def parser_input(input_data):
    """Parser a str input to correct type to work
    
    Args:
        input_data (str): The data of graph coloring instance
    
    Returns:
        graph (nextworx) : Graph
    """
    # node_count (int): Number of nodes
    # edge_count (int): Number of edges
    # edges (List(Tuple(int, int))): List of edges
    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])
    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))
    
    graph = nx.Graph(edges)
    
    return graph

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
