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
        return sum(
            item.value * took if took != -1 else 0 
            for item, took in zip(self.items, state)
        )
    
    def eval_room(self, state):
        return self.capacity - sum(
            item.weight * took if took != -1 else 0
            for item, took in zip(self.items, state) 
        )
    
    def eval_estimate(self, state):
        return sum( 
            item.value * took if took != -1 else item.value 
            for item, took in zip(self.items, state)
        )
    
    def is_solution(self, state):
        '''If state taken has no free vars (representable by -1) the taken is a solution'''
        return not -1 in state.taken

    def is_infeasible(self, state):
        '''If state break capacity constraint'''
        return state.room < 0

    def DFS(self):
        stack = [self.best_state]
        current_state = stack.pop()
        while True:
            # Branch
            try:
                index_branch = current_state.taken.index(-1)
            except ValueError:
                # print('Não ha mais para onde ramificar')
                break
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
            while True:
                try:
                    current_state = stack.pop()
                except IndexError:
                    # print('Não há mais nenhum nó a ser explorado!')
                    break
                
                # Bound for infeasibility
                if self.is_infeasible(current_state):
                    # print('O estado atual é inviável, não há esperança de melhora ao ramificar')
                    continue
                # Bound for optimality
                if current_state.estimate < self.best_state.value:
                    # print('O estado atual tem uma estimativa PIOR que a melhor solução obtida')
                    continue
                if self.is_solution(current_state):
                    if current_state.value > self.best_state.value:
                        self.best_state = current_state
                    continue
                break
        return parser_output(
            self.best_state.value,
            self.best_state.taken,
            optimal=1
        )
            
            


            

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
        print(bnb.DFS())
        
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')