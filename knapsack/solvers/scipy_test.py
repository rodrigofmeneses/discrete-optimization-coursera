from scipy.optimize import linprog
from utils import parser_input

# Max Sum(cx)
# SA. Ax = b
# x 

input_data = '4 11\n8 4\n10 5\n15 8\n4 3'

item_count, capacity, items = parser_input(input_data)

# coeficientes
c = [-1 * item.value for item in items]
A_ub = [[item.weight for item in items]]
b_ub = [capacity]
bounds = [(0, 1) for _ in range(item_count)]
result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds)
print(result)