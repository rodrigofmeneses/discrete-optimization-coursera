import matplotlib.pyplot as plt


def parser_input(input_data):
    """Parser a str input to correct type to work
    
    Args:
        input_data (str): The data of TSP instance
    
    Returns:
        list (tuple) : coordinates
    """
    # parse the input
    lines = input_data.split('\n')

    nodeCount = int(lines[0])

    points = []
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append((float(parts[0]), float(parts[1])))
    
    return points
    


def parser_output(solution, obj, optimal=0):
    """Parser objetive value and decisions variables to specific format to submit assignment to Coursera
    Args:
        solution (list): List of decision variables.
        obj (int): Value of objective function.
        optimal (int): Value 1 if solution is proved optimal. Default is 0.
    
    Returns:
        output_data (str): Specific format to Coursera submission
    """
    output_data = '%.2f' % obj + ' ' + str(optimal) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data

def show_tour(x_sol, positions):
    fig, ax = plt.subplots(2, sharex=True, sharey=True)         # Prepare 2 plots
    ax[0].set_title('Raw nodes')
    ax[1].set_title('Optimized tour')
    ax[0].scatter(positions[:, 0], positions[:, 1])             # plot A
    ax[1].scatter(positions[:, 0], positions[:, 1])             # plot B
    start_node = x_sol[0]
    x_sol = np.append(x_sol, x_sol[0])
    positions = np.vstack((positions, positions[start_node]))
    distance = 0.
    N = len(positions)
    for i in range(N - 1):
        start_pos = positions[start_node]
        # next_node = np.argmax(x_sol[start_node]) # needed because of MIP-approach used for TSP
        next_node = x_sol[i + 1] # needed because of MIP-approach used for TSP
        end_pos = positions[next_node]
        ax[1].annotate("",
                xy=start_pos, xycoords='data',
                xytext=end_pos, textcoords='data',
                arrowprops=dict(arrowstyle="->",
                                connectionstyle="arc3"))
        distance += np.linalg.norm(end_pos - start_pos)
        start_node = next_node

    textstr = "N nodes: %d\nTotal length: %.3f" % (N, distance)
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax[1].text(0.05, 0.95, textstr, transform=ax[1].transAxes, fontsize=14, # Textbox
            verticalalignment='top', bbox=props)

    plt.tight_layout()
    plt.show()