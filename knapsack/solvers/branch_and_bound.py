from collections import namedtuple
from operator import attrgetter
from scipy.optimize import linprog
from solvers.utils import parser_input, parser_output

State = namedtuple('Knapsack', ['taken', 'value', 'room', 'estimate', 'depth'])
# taken: items taken
# value: sum of value of items taken
# room: remain space in knapsack
# estimate: optimistic estimate of value

class BranchAndBound:
    """Branch and Bound algorithm for knapsack 0/1 problem.
    
    Args:
        input_data (str): The data of knapsack instance
    """
    def __init__(self, input_data):
        # Knapsack instante
        self.item_count, self.capacity, self.items = parser_input(input_data)
        # Linear Programming data
        self.c = [-1 * item.value for item in self.items]
        self.A_ub = [[item.weight for item in self.items]]
        self.b_ub = [self.capacity]
        # Upper bound
        self.best_estimate = self.eval_estimate([-1] * self.item_count)
        # Lower Bound
        self.best_state = State(
            taken=[-1] * self.item_count,
            value=0,
            room=self.capacity,
            estimate=self.best_estimate,
            depth=0
        )
    
    def eval_value(self, taken) -> int:
        """ Evaluate the objective function of state given a taken list, named by value.
        
        Args:
            taken (list): List of variables of len of knapsack with values 0, 1 or -1, 
                where in any index 0 if item is a not took, 1 if is took and -1 if is not decided.
        
        Retuns:
            Value of state, internal product with replacement of -1 to 0,
                in knapsack problem is objective function.
        """
        return sum(
            item.value * took if took != -1 else 0 
            for item, took in zip(self.items, taken)
        )
    
    def eval_room(self, taken) -> int:
        """ Evaluate remain weigth in knapsack given a taken list, named by room.

        Args:
            taken (list): List of variables of len of knapsack with values 0, 1 or -1, 
                where in any index 0 if item is a not took, 1 if is took and -1 if is not decided.
            
        Returns:
            Remain weigth in knapsack.
        """
        return self.capacity - sum(
            item.weight * took if took != -1 else 0
            for item, took in zip(self.items, taken) 
        )
    
    def eval_estimate(self, taken) -> float:
        """ Evaluate a optmistic estimate of value given a taken list,
                this estimate is a relaxation of problem based on linear programming.
        
        Args:
            taken (list): List of variables of len of knapsack with values 0, 1 or -1, 
                where in any index 0 if item is a not took, 1 if is took and -1 if is not decided.
        
        Returns:
            Optimistic estimate of value, based of linear programming.
        """
        bounds = [(0, 1) if bound == -1 else (bound, bound) for bound in taken]
        result = linprog(self.c, A_ub=self.A_ub, b_ub=self.b_ub, bounds=bounds)
        return 0 if result['fun'] == None else result['fun'] * -1
    
    def is_solution(self, state) -> bool:
        '''Evaluate if state is a solution.
                Note: Just a solution, no guarantee that is viable.
        
        Args:
            state (State): A namedtuple that represents a state of knapsack problem.
        
        Returns:
            A boolean that indicates if the state is a solution.
        '''
        return not -1 in state.taken

    def is_feasible(self, state) -> bool:
        '''Evaluate if state is feasible.
                Note: Based on capacity constraint, represented by room.
        
        Args:
            state (State): A namedtuple that represents a state of knapsack problem.

        Returns:
            A boolean that indicates if the state is feasable.
        '''
        return state.room >= 0

    def DFS(self):
        ''' Branch based on Deep First Search. This approach mantains a stack of states and explore the tree based on depth search.
                
                'order_to_branch' is the order order of variables to explores based on density items, more density
                items may explored first.
                'depth' variable is the depth of tree that the state is.
                'left' and 'right' are the childrens of current node.
                The pruning is realized under three conditions, infeasible nodes, nodes domain for best solution
                and node better than best solution.
        '''
        stack = [self.best_state]
        current_state = stack.pop()
        order_to_branch = [item.index for item in sorted(self.items, key=attrgetter('density'), reverse=True)]
        depth = current_state.depth
        while True:
            # Branch
            try:
                index_branch = order_to_branch[depth]
            except IndexError:
                # print('N??o ha mais para onde ramificar')
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
                    estimate=self.eval_estimate(right),
                    depth=depth + 1
                )
            )

            stack.append(
                State(
                    taken=left,
                    value=self.eval_value(left),
                    room=self.eval_room(left),
                    estimate=self.eval_estimate(left),
                    depth=depth + 1
                )
            )

            # Bound
            while True:
                try:
                    current_state = stack.pop()
                    depth = current_state.depth
                except IndexError:
                    # print('N??o h?? mais nenhum n?? a ser explorado!')
                    break
                
                # Bound for infeasibility
                if not self.is_feasible(current_state):
                    # print('O estado atual ?? invi??vel, n??o h?? esperan??a de melhora ao ramificar')
                    continue
                # Bound for optimality
                if current_state.estimate < self.best_state.value:
                    # print('O estado atual tem uma estimativa PIOR que a melhor solu????o obtida')
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
    return bnb.DFS()