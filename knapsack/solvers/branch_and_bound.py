from collections import namedtuple
from utils import parser_input, parser_output

State = namedtuple('Knapsack', ['taken', 'value', 'room', 'estimate'])
# taken: items taken
# value: sum of value of items taken
# room: remain space in knapsack
# estimate: optimistic estimate of value

class BranchAndBound:
    def __init__(self, input_data):
        # Knapsack instante
        self.item_count, self.capacity, self.items = parser_input(input_data)
        # Upper bound
        self.best_estimate = sum(item.value for item in self.items)
        # Lower Bound
        self.best_state = State(
            taken=[-1] * self.item_count,
            value=0,
            room=self.capacity,
            estimate=self.best_estimate
        )
    
    def eval_value(self, state):
        if isinstance(state, list):
            return sum(
                item.value * took if took != -1 else 0 
                for item, took in zip(self.items, state)
            )
        return sum(item.value * took for item, took in zip(self.items, state.taken))
    
    def eval_room(self, state):
        if isinstance(state, list):
            return self.capacity - sum(
                item.weight * took if took != -1 else 0
                for item, took in zip(self.items, state) 
            )
        return self.capacity - sum(item.weight * took for item, took in zip(self.items, state.taken))
    
    def eval_estimate(self, state):
        return sum( 
            item.value * took if took != -1 else item.value 
            for item, took in zip(self.items, state)
        )
    
    def is_solution(self, state):
        '''If state taken has no free vars (representable by -1) the taken is a solution'''
        return not -1 in state.taken

    def is_feasible(self, state):
        '''If state taken is a solution and not break capacity constraint'''
        if self.is_solution(state):
            return state.capacity >= 0
        return False

    def DFS(self):
        stack = [self.best_state]
        while stack:
            current_state = stack.pop()
            # Bound
            # Has 3 types of bounds
            # Optimality
            # if solution is feasible and the value is best of current best
            # Infeasibility
            # if solution is infeasible
            # Upper bound
            # if best expectate of sulution is less of upper bound
            # upper bound = sum of all values...
            # if self.is_feasible(current_state):
            #     if self.value(current_state) > self.value(self.best_state):
            #         self.best_state = current_state


            # Branch
            try:
                index_branch = current_state.taken.index(-1)
            except ValueError:
                print('Não ha mais para onde ramificar')
                continue
            left = current_state.taken.copy()
            left[index_branch] = 1
            right = current_state.taken.copy()
            right[index_branch] = 0

            stack.append(
                State(
                    taken=right,
                    value=self.eval_value(right),
                    room=self.eval_room(right),
                    estimate=self.eval_estimate(right)
                )
            )

            stack.append(
                State(
                    taken=left,
                    value=self.eval_value(left),
                    room=self.eval_room(left),
                    estimate=self.eval_estimate(left)
                )
            )

            # Bound

def main(input_data):
    bnb = BranchAndBound(input_data)

    
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        # main(input_data)
        bnb = BranchAndBound(input_data)
        bnb.DFS()
        
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')