import sys
import numpy as np

from numpy.linalg import norm
from solvers.utils import parser_input, parser_output, show_tour


def nearest_neighbor(distance_matrix):
    tmp_dm = distance_matrix.copy()
    # Complete tour
    tour = [0]
    current_city = 0
    for _ in range(len(distance_matrix) - 1):
        next_city = np.argmin(tmp_dm[current_city])
        tmp_dm[current_city, :] = np.inf
        tmp_dm[:, current_city] = np.inf
        current_city = next_city
        tour.append(next_city)
    return tour

def two_opt_swap(tour, i, j):
    _tour = tour.copy()
    _tour[i:j] = _tour[i:j][::-1]
    return _tour

def tour_distance(tour, distance_matrix):
    distance = distance_matrix[tour[-1], tour[0]]
    for index in range(0, len(tour) - 1):
        distance += distance_matrix[tour[index], tour[index+1]]
    return distance

def two_opt(input_data):
    points = np.array(parser_input(input_data))
    node_count = len(points)
    distance_matrix = np.zeros((node_count, node_count))
    for i in range(node_count):
        for j in range(i, node_count):
            if i == j:
                distance_matrix[i, j] = np.inf
                continue
            distance = norm(points[i] - points[j])
            distance_matrix[i, j] = distance
            distance_matrix[j, i] = distance

    # Solução inicial, vou botar um NN
    best_tour = nearest_neighbor(distance_matrix)
    best_tour_distance = tour_distance(best_tour, distance_matrix)
    improved = True 
    while improved:
        improved = False

        for i in range(node_count):
            for j in range(i + 1, node_count - 1):
                # Faz a troca, verifica se o tour é melhor
                new_tour = two_opt_swap(best_tour, i, j)
                new_tour_distance = tour_distance(new_tour, distance_matrix)
                if new_tour_distance < best_tour_distance:
                    best_tour = new_tour
                    best_tour_distance = new_tour_distance
                    improved = True

    # show_tour(best_tour, points)
    output_data = parser_output(best_tour, best_tour_distance)
    return output_data

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(two_opt(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')