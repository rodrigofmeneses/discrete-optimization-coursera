import sys
import numpy as np

from numpy.linalg import norm 
from solvers.utils import parser_input, parser_output


def nearest_neighbor(input_data):
    points = np.array(parser_input(input_data))
    node_count = len(points)
    distance_matrix = np.zeros((node_count, node_count))
    
    # diagonal to infinite
    for i in range(node_count): distance_matrix[i, j] = np.inf
    
    for i in range(node_count):
        for j in range(i + 1, node_count):
            distance = norm(points[i] - points[j])
            distance_matrix[i, j] = distance
            distance_matrix[j, i] = distance

    # Complete tour
    tmp_dm = distance_matrix.copy()

    tour = [0]
    current_city = 0
    for _ in range(len(distance_matrix) - 1):
        next_city = np.argmin(tmp_dm[current_city])
        tmp_dm[current_city, :] = np.inf
        tmp_dm[:, current_city] = np.inf
        current_city = next_city
        tour.append(next_city)

    distance = distance_matrix[tour[-1], tour[0]]
    for index in range(0, len(tour) - 1):
        distance += distance_matrix[tour[index], tour[index + 1]]

    # show_tour(best_tour, points)
    output_data = parser_output(tour, distance)
    return output_data

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(nearest_neighbor(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')