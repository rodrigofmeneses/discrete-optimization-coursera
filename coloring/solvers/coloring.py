import sys
import time
from ortools.sat.python import cp_model
from solvers.utils import parser_input, parser_output

def greedy(input_data):
    """ Greedly select colors based on neigbhood

    Args:
        input_data (str): The data of coloring instance
    
    Returns:
        output_data (str): Specific format to submit assignment to Coursera
    """
    # Create Graph object using networkx
    graph = parser_input(input_data)
    # Assign colors variables to -1, its mean not choosed color
    colors = [-1] * graph.number_of_nodes()
    # Fix first color for first node by 0
    colors[0] = 0

    # Order nodes by degree
    max_degree = max(graph.degree(), key=lambda degree: degree[1])[1]
    nodes_sorted_by_degree = [
        node for node, _ in sorted(graph.degree(), reverse=True, key=lambda degree: degree[1])
    ]

    # Explore all nodes by decrease order of degrees
    # and choose a diferent color of neigbhood, to minor
    for node in nodes_sorted_by_degree:
        adj_colors = [colors[nbr] for nbr in list(graph.neighbors(node))]
        for c in range(max_degree):
            if not c in adj_colors:
                colors[node] = c
                break

    output_data = parser_output(max(colors) + 1, colors, 0)
    return output_data

class ColoringSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, colors):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__colors = colors
        self.__solution_count = 0
        self.__start_time = time.time()

    def solution_count(self):
        return self.__solution_count

    def on_solution_callback(self):
        current_time = time.time()
        print('Solution %i, time = %f s' %
              (self.__solution_count, current_time - self.__start_time))
        self.__solution_count += 1

        all_colors = range(len(self.__colors))
        for i in all_colors:
            print(self.Value(self.__colors[i]), end=' ')
        print()


def constraint_programming(input_data):
    graph = parser_input(input_data)
    node_count = graph.number_of_nodes()
    max_degree = max(graph.degree(), key=lambda degree: degree[1])[1]

    model = cp_model.CpModel()
    # Variables
    colors = [
        model.NewIntVar(0, max_degree, f'c{i}') for i in range(node_count)
    ]
    
    # Constraints
    for i, j in graph.edges:
        model.Add(colors[i] != colors[j])
    
    # Break Symmetry
    # WEAK
    for i in range(node_count):
        model.Add(colors[i] <= i + 1)

    # Objective Function
    max_colors = model.NewIntVar(0, max_degree, 'number of colors')
    model.AddMaxEquality(max_colors, colors)
    model.Minimize(max_colors)
    # model.AddDecisionStrategy(colors, cp_model.CHOOSE_FIRST, cp_model.SELECT_MIN_VALUE)

    solver = cp_model.CpSolver()
    solution_printer = ColoringSolutionPrinter(colors)
    solver.parameters.max_time_in_seconds = 2400.0
    # solver.parameters.enumerate_all_solutions = True

    solver.Solve(model, solution_printer)
    # solver.Solve(model)

    # Statistics.
    print('\nStatistics')
    print(f'  conflicts      : {solver.NumConflicts()}')
    print(f'  branches       : {solver.NumBranches()}')
    print(f'  wall time      : {solver.WallTime()} s')
    print(f'  bounds         : {solver.BestObjectiveBound()}')
    print(f'  solutions found: {solution_printer.solution_count()}')
    print()

    output_data = parser_output(
        int(solver.ObjectiveValue() + 1) , 
        (str(solver.Value(colors[i])) for i in range(node_count)), 
        '0'
    )
    return output_data

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        # print(greed(input_data))
        print(constraint_programming(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

